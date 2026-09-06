#include "sequence.hpp"
#include <iostream>

notebook::Integer integer(const std::string& word) {
    const auto start = !word.empty() && (word.front() == '+' || word.front() == '-') ? 1u : 0u;
    if (start == word.size() ||
        !std::all_of(word.begin() + start, word.end(), [](char c) { return c >= '0' && c <= '9'; })) {
        throw std::invalid_argument("invalid integer token");
    }
    return std::stoll(word);
}

notebook::Sequence numbers(const std::string& text) {
    notebook::Sequence result;
    if (text.empty()) return result;
    std::size_t begin = 0;
    while (true) {
        const auto end = text.find(',', begin);
        result.push_back(integer(text.substr(begin, end - begin)));
        if (end == std::string::npos) break;
        begin = end + 1;
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
            const auto actual = notebook::evaluate(fields[0], numbers(fields[2]), integer(fields[1]));
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
