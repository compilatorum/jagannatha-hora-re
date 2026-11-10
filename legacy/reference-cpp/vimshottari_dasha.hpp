/**
 * @file vimshottari_dasha.hpp
 * @brief Clean C++20 re-implementation of the Jagannatha Hora Vimshottari Dasha Engine.
 * Reconstructed from decompiled Borland C++ Builder binaries.
 */

#ifndef VIMSHOTTARI_DASHA_HPP
#define VIMSHOTTARI_DASHA_HPP

#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <iomanip>

namespace JyotishEngine {

enum GrahaId : int {
    KETU = 0,
    VENUS = 1,
    SUN = 2,
    MOON = 3,
    MARS = 4,
    RAHU = 5,
    JUPITER = 6,
    SATURN = 7,
    MERCURY = 8,
    GRAHA_TOTAL = 9
};

inline const std::string GRAHA_NAMES[9] = {
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
};

inline const double DASHA_YEARS[9] = {
    7.0, 20.0, 6.0, 10.0, 7.0, 18.0, 16.0, 19.0, 17.0
};

constexpr double TOTAL_DASHA_CYCLE = 120.0;
constexpr double NAKSHATRA_SPAN_DEG = 360.0 / 27.0; // 13.333333333333334 degrees (800 arcmin)
constexpr double DEFAULT_DAYS_PER_YEAR = 365.2425;  // Gregorian average year

struct DashaPeriod {
    int level;                      // 1 = MD, 2 = AD, 3 = PD, 4 = SD, 5 = PAD
    std::vector<int> lords;         // Chain of lords: [MD], [MD, AD], [MD, AD, PD], etc.
    double start_jd;                // Julian Day start
    double end_jd;                  // Julian Day end
    double duration_days;           // Duration in days
    double duration_years;          // Duration in astrological years
};

class VimshottariDashaEngine {
public:
    explicit VimshottariDashaEngine(double days_per_year = DEFAULT_DAYS_PER_YEAR)
        : m_days_per_year(days_per_year) {}

    void CalculateBirthBalance(double moon_lon,
                               int& nakshatra_idx,
                               double& balance_fraction,
                               int& birth_lord_idx) const {
        double lon = std::fmod(moon_lon, 360.0);
        if (lon < 0.0) lon += 360.0;

        nakshatra_idx = static_cast<int>(std::floor(lon / NAKSHATRA_SPAN_DEG));
        if (nakshatra_idx > 26) nakshatra_idx = 26;

        double nak_start = nakshatra_idx * NAKSHATRA_SPAN_DEG;
        double elapsed_arc = lon - nak_start;
        balance_fraction = 1.0 - (elapsed_arc / NAKSHATRA_SPAN_DEG);
        birth_lord_idx = nakshatra_idx % 9;
    }

    std::vector<DashaPeriod> GenerateMahadashas(double birth_jd, double moon_lon) const {
        int nak_idx = 0;
        double balance_frac = 0.0;
        int birth_lord = 0;
        CalculateBirthBalance(moon_lon, nak_idx, balance_frac, birth_lord);

        std::vector<DashaPeriod> result;
        double current_jd = birth_jd;

        for (int i = 0; i < 9; ++i) {
            int lord = (birth_lord + i) % 9;
            double full_years = DASHA_YEARS[lord];
            double actual_years = (i == 0) ? (full_years * balance_frac) : full_years;
            double span_days = actual_years * m_days_per_year;

            DashaPeriod p;
            p.level = 1;
            p.lords = {lord};
            p.start_jd = current_jd;
            p.end_jd = current_jd + span_days;
            p.duration_years = actual_years;
            p.duration_days = span_days;

            result.push_back(p);
            current_jd = p.end_jd;
        }

        return result;
    }

    std::vector<DashaPeriod> SubdividePeriod(const DashaPeriod& parent) const {
        std::vector<DashaPeriod> children;
        int next_level = parent.level + 1;
        if (next_level > 5) return children;

        int parent_lord = parent.lords.back();
        double current_jd = parent.start_jd;
        double parent_duration_days = parent.duration_days;

        for (int i = 0; i < 9; ++i) {
            int child_lord = (parent_lord + i) % 9;
            double child_fraction = DASHA_YEARS[child_lord] / TOTAL_CYCLE_YEARS;
            double child_days = parent_duration_days * child_fraction;

            DashaPeriod child;
            child.level = next_level;
            child.lords = parent.lords;
            child.lords.push_back(child_lord);
            child.start_jd = current_jd;
            child.end_jd = current_jd + child_days;
            child.duration_days = child_days;
            child.duration_years = child_days / m_days_per_year;

            children.push_back(child);
            current_jd = child.end_jd;
        }

        return children;
    }

private:
    double m_days_per_year;
};

} // namespace JyotishEngine

#endif // VIMSHOTTARI_DASHA_HPP
