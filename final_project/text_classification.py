import pandas as pd
import json

# TODO: linux space character used

class Model:
    def __init__(self, filepath):
        pass
        # all_data = None
        # with open(filepath) as f:
        #     all_data = f.readlines()
        # title, text = all_data[0].split('@@@@@@@@@@')
        # with open('temp.txt', 'w') as f:
        #     f.write(all_data[2])
        #     f.write(all_data[10])
        # title.encode('utf-8')
        # print(all_data)
        # for i in title:
            # print(int(i))

        # t = 'اقتصاد'
        # title.
        # print(len(title))
        # print(len(t))
        # print(len('اقتصاد'))
        # print(title == 'اقتصاد')
        # print(t)
        # print(title)
        # print(text)

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

def main():
    # this lines saves all the words and titles in seperate files
    # Model.save_words('HAM-Train.txt', 'words.txt', 'titles.txt', say=True)

    # this line stores the number of word occurences in each context in a csv file
    # Model.count_words_for_titles('titles.txt', 'words.txt', 'HAM-Train.txt', 'word_count.csv', say=True)
    # a = {1: 'a', 2: 'b'}
    # print(a.get(3, None))

    x = Model('xxx')
    x.build_model('HAM-Train.txt', True)
    # pass

    # dict = {'a': [1, 2, 3], 'b': [1, 2, 4]}
    # a = pd.DataFrame.from_dict(dict)
    # pd.DataFrame.to_csv(a, path_or_buf='test_csv.csv', index=False)
    # print(a)
    # a = {i:i + 1 for i in range(10)}
    # print(a)

    
    # a = 'hello\n'
    # b = a.replace('\n', '', 1)
    # print(a)
    # print(b)
    # print(b)
    # a = 'بزرگترین'
    # b = 'بزرگتران'
    # print(a == b)

if __name__ == '__main__':
    main()
