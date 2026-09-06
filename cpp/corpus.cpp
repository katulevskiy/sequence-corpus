#include "sequence.hpp"
#include <iostream>
#include <sstream>

notebook::Sequence numbers(const std::string& text) {
    notebook::Sequence result;
    if (text.empty()) return result;
    std::istringstream stream(text);
    std::string word;
    while (std::getline(stream, word, ',')) {
        std::size_t used = 0;
        const auto value = std::stoll(word, &used);
        if (used != word.size()) throw std::invalid_argument("invalid integer");
        result.push_back(value);
    }
    return result;
}

int main() {
    std::size_t count = 0;
    std::string line;
    try {
        while (std::getline(std::cin, line)) {
            std::vector<std::string> fields;
            std::size_t begin = 0;
            while (true) {
                const auto end = line.find('\t', begin);
                fields.push_back(line.substr(begin, end - begin));
                if (end == std::string::npos) break;
                begin = end + 1;
            }
            if (fields.size() != 4) throw std::invalid_argument("expected four fields");
            const auto actual = notebook::evaluate(fields[0], numbers(fields[2]), std::stoll(fields[1]));
            if (actual != numbers(fields[3])) {
                std::cerr << "Corpus row " << count + 1 << " failed\n";
                return 1;
            }
            ++count;
        }
    } catch (const std::exception& error) {
        std::cerr << "Corpus row " << count + 1 << ": " << error.what() << '\n';
        return 1;
    }
    std::cout << "C++: " << count << " corpus cases passed\n";
}
