#pragma once

#include <algorithm>
#include <cstdint>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace notebook {
using Integer = std::int64_t;
using Sequence = std::vector<Integer>;

// The caller must keep intermediate arithmetic within signed 64-bit range.
inline Sequence evaluate(const std::string& operation, const Sequence& values,
                         Integer argument = 0) {
    if (operation == "sum") {
        return {std::accumulate(values.begin(), values.end(), Integer{0})};
    }
    if (operation == "prefix") {
        Sequence result(values.size());
        std::partial_sum(values.begin(), values.end(), result.begin());
        return result;
    }
    if (operation == "diff") {
        Sequence result;
        for (std::size_t index = 1; index < values.size(); ++index) {
            result.push_back(values[index] - values[index - 1]);
        }
        return result;
    }
    if (operation == "unique") {
        auto result = values;
        std::sort(result.begin(), result.end());
        result.erase(std::unique(result.begin(), result.end()), result.end());
        return result;
    }
    if (operation == "runs") {
        Sequence result;
        for (const auto value : values) {
            if (!result.empty() && result[result.size() - 2] == value) {
                ++result.back();
            } else {
                result.push_back(value);
                result.push_back(1);
            }
        }
        return result;
    }
    if (operation == "rotate") {
        if (argument < 0) throw std::invalid_argument("rotation must be nonnegative");
        auto result = values;
        if (!result.empty()) {
            const auto shift = static_cast<std::size_t>(argument) % result.size();
            std::rotate(result.begin(), result.begin() + shift, result.end());
        }
        return result;
    }
    if (operation == "windows") {
        if (argument < 0) throw std::invalid_argument("window must be nonnegative");
        const auto width = static_cast<std::size_t>(argument);
        if (width == 0 || width > values.size()) return {};
        Integer total = std::accumulate(values.begin(), values.begin() + width, Integer{0});
        Sequence result{total};
        for (std::size_t index = width; index < values.size(); ++index) {
            total += values[index] - values[index - width];
            result.push_back(total);
        }
        return result;
    }
    if (operation == "bound") {
        return {std::count_if(values.begin(), values.end(),
                             [argument](Integer value) { return value < argument; })};
    }
    if (operation == "clamp") {
        if (argument < 0) throw std::invalid_argument("clamp limit must be nonnegative");
        Sequence result;
        result.reserve(values.size());
        for (const auto value : values) {
            result.push_back(std::clamp(value, -argument, argument));
        }
        return result;
    }
    if (operation == "reverse") return Sequence(values.rbegin(), values.rend());
    throw std::invalid_argument("unknown operation: " + operation);
}
} // namespace notebook
