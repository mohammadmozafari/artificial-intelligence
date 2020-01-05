import pandas as pd
import json
import math

class Model:
    def __init__(self, lambda1, lambda2):
        self.lam1 = lambda1
        self.lam2 = lambda2

    @staticmethod
    def save_words(source, target1, target2, say=False):
        """
        This utility method helps us to extract words and titles from raw text files.
        Inputs
        - source: the filepath for raw text
        - target1: the filepath in which we store words
        - target2: the filepath in which we store titles
        - say: if true then function prints progress
        """
        all_words = set()
        titles = set()

        with open(source) as f:
            lines = f.readlines()
            for (i, line) in enumerate(lines):
                if say: print('reading line', i + 1)
                a, b = line.split('@@@@@@@@@@')
                titles.add(a)
                words = b.split(' ')
                for w in words:
                    if w == ' ' or w == '' or w == '\n':
                        continue
                    all_words.add(w)
        
        print(str(len(all_words)), 'words found.')
        print(str(len(titles)), 'titles found.')
        with open(target1, 'w') as f:
            for w in all_words:
                f.write('%s\n' % w)
            f.write('---------- %d words.' % len(all_words))
        with open(target2, 'w') as f:
            for t in titles:
                f.write('%s\n' % t)
            f.write('---------- %d titles.' % len(titles))
        print('writing done.')

    @staticmethod
    def count_words_for_titles(titles_file, words_file, text_file, csv_file, say=False):
        """
        A utility method that goes through text file and counts the occurrence of each word
        in its corresponding category and saves the result in a csv file.
        Inputs:
        - titles_file: filepath containing the titles of the texts
        - words_file: filepath containing all words
        - text_file: raw text file
        - csv_file: filepath in which we store the result
        - say: if true then function prints progress
        """
        titles = None
        words_dic = {}
        dic = None

        with open(titles_file) as f:
            titles = f.readlines()
            titles = titles[:-1]
        with open(words_file) as f:
            i = 0
            while True:
                line = f.readline()
                if line.startswith('--'): break
                words_dic[line.replace('\n', '', 1)] = i
                i += 1
        dic = {titles[i].replace('\n', '', 1): [0 for j in range(len(words_dic))] for i in range(len(titles))}

        i = 1
        with open(text_file) as f:
            while True:
                if say: print('reading line', i)
                i += 1
                line = f.readline()
                if len(line) < 5:
                    break
                a, b = line.split('@@@@@@@@@@')
                ws = b.split(' ')
                for w in ws:
                    if w == ' ' or w == '' or w == '\n':
                        continue
                    dic[a][words_dic[w]] += 1
        dataframe = pd.DataFrame.from_dict(dic)
        pd.DataFrame.to_csv(dataframe, csv_file, index=False, encoding='ansi')
        print('writing done')

    def build_model(self, text_file, say=True):
        """
        This method builds the model which we use later to compute probability
        of a class for a text. (Text Classification)
        """
        model = {}
        with open(text_file) as f:
            lines = f.readlines()
            for (i, line) in enumerate(lines):
                if say: print('reading line', i + 1)
                title, text = line.split('@@@@@@@@@@')
                # new paragraph
                category = model.get(title, None)
                if category == None:
                    model[title] = [0, 0, {'<sos>': 0}, {}]
                    category = model[title]
                category[0] += 1
                category[1] += 1
                category[2]['<sos>'] += 1
                # count words of the paragraph
                words = text.split(' ')
                previous_word = '<sos>'
                for word in words:
                    if word == ' ' or word == '' or word == '\n':
                        continue
                    
                    category_unary = category[2]
                    category_unary[word] = 1 if category_unary.get(word, None) == None else (category_unary[word] + 1)

                    binary = previous_word + '-' + word
                    category_binary = category[3]
                    category_binary[binary] = 1 if category_binary.get(binary, None) == None else (category_binary[binary] + 1)
                    
                    previous_word = word
        with open('result.json', 'w') as fp:
            json.dump(model, fp, indent=4)
        self.model = model
    
    def load_model(self, json_file):
        """
        This method imports trained model from a json file into a dictionary
        """
        with open(json_file) as f:
            self.model = json.load(f)

    def test(self, text_file, say=True):
        """
        This method tests the probablistic model on test set and returns the results
        """
        predictions = []
        with open(text_file) as f:
            lines = f.readlines()
            for (i, line) in enumerate(lines):
                if say: print('reading line', i + 1)
                title, text = line.split('@@@@@@@@@@')
                max_p = -1
                prediction = None
                for category in self.model:
                    p = self.estimate_probability(text, category)
                    if p > max_p:
                        max_p = p
                        prediction = category
                predictions.append((title, prediction))
        return predictions

    def estimate_probability(self, text, category):
        p = 0.0
        p += self.log_p_class(category)
        words = text.split(' ')
        for i in range(len(words)):
            if words[i] == ' ' or words[i] == '' or words[i] == '\n':
                continue
            if i == 0:
                binary_exp = '<sos>-' + words[i]
            else:
                binary_exp = words[i - 1] + '-' + words[i]
            score = self.lam1 * self.model[category][3].get(binary_exp, 0)
            score += self.lam2 * self.model[category][2].get(words[i], 0)
            score += 1e-5
            p += math.log(score)
        return p

    def log_p_class(self, category):
        all_lines = 0
        for cat in self.model:
            all_lines += self.model[cat][0]
        return math.log(self.model[category][0] / all_lines)

    def calculate_metrics(self, preds):
        precision = {c: 0 for c in self.model}
        recall = {c: 0 for c in self.model}
        f1 = {c: 0 for c in self.model}

        num_class = len(self.model)
        tp = {c: 1e-10 for c in self.model}
        prec_denom = {c: 1e-10 for c in self.model}
        rec_denom = {c: 1e-10 for c in self.model}
        for correct, guess in preds:
            if correct == guess:
                tp[correct] += 1
                prec_denom[correct] += 1
                rec_denom[correct] += 1
            else:
                prec_denom[guess] += 1
                rec_denom[correct] += 1
        
        for c in self.model:
            precision[c] = tp[c] / prec_denom[c]
            recall[c] = tp[c] / rec_denom[c]
            f1[c] = (2 * precision[c] * recall[c]) / (precision[c] + recall[c])
        return precision, recall, f1

def main():
    # this lines saves all the words and titles in seperate files
    # Model.save_words('HAM-Train.txt', 'words.txt', 'titles.txt', say=True)

    # this line stores the number of word occurences in each context in a csv file
    # Model.count_words_for_titles('titles.txt', 'words.txt', 'HAM-Train.txt', 'word_count.csv', say=True)

    model = Model(0.5, 0.5)

    # this line builds a model using data and stores the result in json file
    # x.build_model('HAM-Train.txt', True)

    model.load_model('result.json')
    # print(x.model)
    pres = model.test('HAM-Test.txt', say=True)
    precision, recall, f1 = model.calculate_metrics(pres)

    print()
    print('=====================================')
    for c in model.model:
        print(c)
        print('precision', precision[c])
        print('recall', recall[c])
        print('f1', f1[c])
        print('---------------------------')

if __name__ == '__main__':
    main()
