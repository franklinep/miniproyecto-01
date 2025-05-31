class BytePairEncoding:
    def __init__(self, num_merges):
        self.num_merges = num_merges
        self.vocab = {}
        self.merges = []

    def train(self, corpus):
        tokenized_corpus = []
        initial_chars = set()
        for word in corpus:
            tokens = list(word) # divide en caracteres
            tokenized_corpus.append(tokens)
            for char in tokens:
                initial_chars.add(char)

        # creamos nuestro vocab inicial
        self.vocab = {char: char for char in initial_chars}

        for merge_step in range(1, self.num_merges + 1):
            pairs = self.get_pair_frequencies(tokenized_corpus)

            most_frequent_pair = max(pairs, key=pairs.get)
            new_token = ''.join(most_frequent_pair)

            self.vocab[new_token] = new_token
            self.merges.append(most_frequent_pair)

            tokenized_corpus = self.replace_pairs_in_corpus(tokenized_corpus, most_frequent_pair, new_token)


    def get_pair_frequencies(self, tokenized_corpus):
        pairs = {}
        for tokens in tokenized_corpus:
            for i in range(len(tokens) - 1):
                pair = (tokens[i], tokens[i + 1])
                pairs[pair] = pairs.get(pair, 0) + 1
        return pairs

    def replace_pairs_in_corpus(self, tokenized_corpus, pair_to_replace, new_token):
        new_corpus = []
        for tokens_in_word in tokenized_corpus:
            new_word_tokens = []
            i = 0
            while i < len(tokens_in_word):
                if i < len(tokens_in_word) - 1 and \
                    (tokens_in_word[i], tokens_in_word[i+1])== pair_to_replace:
                    new_word_tokens.append(new_token)
                    i += 2
                else:
                    new_word_tokens.append(tokens_in_word[i])
                    i += 1
            new_corpus.append(new_word_tokens)
        return new_corpus

    def tokenize(self, word_to_tokenize):
        tokens = list(word_to_tokenize)
        # aplicamos las fusiones guardadas en el orden en que fueron agregadas
        for pair_to_merge in self.merges:
            new_token_str = "".join(pair_to_merge)
            i = 0
            new_tokens_after_this_merge_pass = []
            while i < len(tokens):
                if i < len(tokens) - 1 and \
                    (tokens[i], tokens[i+1]) == pair_to_merge:
                    new_tokens_after_this_merge_pass.append(new_token_str)
                    i += 2
                else:
                    new_tokens_after_this_merge_pass.append(tokens[i])
                    i += 1

            tokens = new_tokens_after_this_merge_pass
        return tokens

    def get_vocabulary(self):
        return self.vocab
