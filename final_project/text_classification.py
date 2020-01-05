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
        all_words = set()
        titles = set()

        with open(source) as f:
            lines = f.readlines()
            for (i, line) in enumerate(lines):
                if say: print('reading line', i + 1)
                a, b = line.split('@@@@@@@@@@')
                
                if a not in titles:
                    titles.add(a)
                words = a.split(' ')
                for w in words:
                    if w == ' ' or w == '' or w == '\n':
                        continue
                    if w not in all_words:
                        all_words.add(w)
                words = b.split(' ')
                for w in words:
                    if w == ' ' or w == '' or w == '\n':
                        continue
                    if w not in all_words:
                        all_words.add(w)
        
        print(str(len(all_words)), 'words found.')
        print(str(len(titles)), 'titles found.')
        with open(target1, 'w') as f:
            for i, w in enumerate(all_words):
                f.write('%d-%s\n' % ((i+1), w))
            f.write('----END----')
        with open(target2, 'w') as f:
            for i, w in enumerate(titles):
                f.write('%d-%s\n' % ((i+1), w))
            f.write('----END----')
        print('writing done.')

    # @staticmethod
    # def get_titles():
    #     return ['اقتصاد', 'سیاست']

def main():
    # this lines saves all the words and titles in seperate files
    # Model.save_words('HAM-Train.txt', 'words.txt', 'titles.txt', say=True)
    pass

if __name__ == '__main__':
    main()
