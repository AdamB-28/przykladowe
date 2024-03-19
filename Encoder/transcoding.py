import string

class CharVectorConverter:
    def __init__(self):
        self.char_to_vector = {}
        self.vector_to_char = {}
        self._populate_mappings()

    def _populate_mappings(self):
        # Populate with uppercase English letters
        for i, char in enumerate(string.ascii_uppercase, 1):
            self.char_to_vector[char] = [1, i // 10, i % 10]

        # Populate with lowercase English letters
        for i, char in enumerate(string.ascii_lowercase, 1):
            self.char_to_vector[char] = [2, i // 10, i % 10]

        # Populate with numbers
        for i, char in enumerate(string.digits, 1):
            self.char_to_vector[char] = [3, i // 10, i % 10]

        # Define and populate with punctuation and space
        punctuations = " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        for i, char in enumerate(punctuations, 1):
            self.char_to_vector[char] = [4, i // 10, i % 10]

        # Adding lowercase Polish letters
        polish_letters_lower = "ąćęłńóśźż"
        for i, char in enumerate(polish_letters_lower, 1):
            self.char_to_vector[char] = [5, i // 10, i % 10]

        # Adding uppercase Polish letters
        polish_letters_upper = "ĄĆĘŁŃÓŚŹŻ"
        for i, char in enumerate(polish_letters_upper, 1):
            self.char_to_vector[char] = [6, i // 10, i % 10]

        # Create reverse mapping
        self.vector_to_char = {tuple(value): key for key, value in self.char_to_vector.items()}
    
    def sentence_to_vectors(self, sentence):
        vectors = []
        for char in sentence:
            if char in self.char_to_vector:  # Check if the character has a corresponding vector
                vector = self.char_to_vector[char]  # Get the vector for the character
                vectors.append(vector)
        return vectors


    def vectors_to_sentence(self, vectors):
        sentence = "" 
        for vector in vectors:
            vector_tuple = tuple(vector)
            if vector_tuple in self.vector_to_char:
                char = self.vector_to_char[vector_tuple]
                sentence += char
        return sentence


if __name__ == "__main__":
    # Example usage
    converter = CharVectorConverter()
    sentence = "Hello, Świat! 123 Ł"
    vectors = converter.sentence_to_vectors(sentence)
    print("Sentence to vectors:", vectors)

    reconstructed_sentence = converter.vectors_to_sentence(vectors)
    print("Vectors to sentence:", reconstructed_sentence)