#!/usr/bin/env python
"""
Generate per-country HTML map reports under reports/country/<alpha2>/
Each report shows a folium map with cemetery markers:
  - Green: all soldiers in the cemetery have photos
  - Red: at least one soldier is missing a photo
"""

import os
import sys
import django

# Bootstrap Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

import folium
from django.db.models import Q, Count
from cmp.models import Country, Cemetery, SoldierDeath


def cemetery_photo_status(cemetery):
    """Return (total_soldiers, soldiers_with_photo) for a cemetery."""
    deaths = SoldierDeath.objects.filter(cemetery=cemetery)
    total = deaths.count()
    with_photo = deaths.exclude(Q(image="") | Q(image__isnull=True)).count()
    return total, with_photo


def build_country_map(country):
    """Build a folium Map for a country's cemeteries. Returns (map, stats) or None."""
    cemeteries = Cemetery.objects.filter(country=country)
    if not cemeteries.exists():
        return None

    valid_cemeteries = []
    for cem in cemeteries:
        try:
            lat = float(cem.latitude)
            lon = float(cem.longitude)
            if lat == 0 and lon == 0:
                continue
            valid_cemeteries.append((cem, lat, lon))
        except (ValueError, TypeError):
            continue

    if not valid_cemeteries:
        return None

    lats = [lat for _, lat, _ in valid_cemeteries]
    lons = [lon for _, _, lon in valid_cemeteries]
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    # Fit bounds to show all markers
    if len(valid_cemeteries) > 1:
        m.fit_bounds([[min(lats), min(lons)], [max(lats), max(lons)]])

    total_cemeteries = 0
    photos_complete = 0
    photos_needed = 0

    for cem, lat, lon in valid_cemeteries:
        total, with_photo = cemetery_photo_status(cem)
        total_cemeteries += 1

        if total == 0:
            # No soldiers recorded — treat as needing photos
            color = "red"
            icon = "camera"
            status_text = "No soldiers recorded"
            photos_needed += 1
        elif with_photo >= total:
            color = "green"
            icon = "ok-sign"
            status_text = f"All {total} photos complete"
            photos_complete += 1
        else:
            color = "red"
            icon = "camera"
            missing = total - with_photo
            status_text = f"{missing} of {total} photos needed"
            photos_needed += 1

        popup_html = (
            f"<b>{cem.name}</b><br>"
            f"{status_text}<br>"
            f"<small>Lat: {lat:.4f}, Lon: {lon:.4f}</small>"
        )

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=cem.name,
            icon=folium.Icon(color=color, icon=icon),
        ).add_to(m)

    stats = {
        "total": total_cemeteries,
        "complete": photos_complete,
        "needed": photos_needed,
    }
    return m, stats


def generate_reports():
    base_dir = os.path.join(os.path.dirname(__file__), "..", "reports", "country")
    os.makedirs(base_dir, exist_ok=True)

    countries = Country.objects.filter(cemeteries__isnull=False).distinct().order_by("alpha2")
    generated = 0

    for country in countries:
        alpha2 = country.alpha2.lower()
        if not alpha2:
            continue

        result = build_country_map(country)
        if result is None:
            continue

        m, stats = result
        country_dir = os.path.join(base_dir, alpha2)
        os.makedirs(country_dir, exist_ok=True)

        output_path = os.path.join(country_dir, "index.html")
        # Add CMP masthead logo and title/legend above the map
        title_html = f"""
        <div style="font-family: Arial, sans-serif; padding: 10px; text-align: center;">
            <a href="/">
                <img src="/static/cmp/cmp-masthead.svg" alt="Corps of Military Police" style="max-width: 400px; width: 100%; margin-bottom: 10px;">
            </a>
            <h2>{country.flag} {country.name} ({country.alpha2})</h2>
            <p>Cemeteries: {stats['total']} &nbsp;|&nbsp;
               <span style="color: green;">&#11044;</span> Photos complete: {stats['complete']} &nbsp;|&nbsp;
               <span style="color: red;">&#11044;</span> Photos needed: {stats['needed']}</p>
            <p style="font-size: 0.85em; color: #666;">
                <span style="color: green;">&#9679;</span> Green = all memorial photos exist &nbsp;&nbsp;
                <span style="color: red;">&#9679;</span> Red = photos still needed
            </p>
        </div>
        """
        m.get_root().html.add_child(folium.Element(title_html))

        # Ensure browser sends Referer header for OSM tile requests
        referrer_meta = '<meta name="referrer" content="no-referrer-when-downgrade">'
        m.get_root().header.add_child(folium.Element(referrer_meta))

        m.save(output_path)
        generated += 1
        print(f"  {country.alpha2} {country.name}: {stats['total']} cemeteries → {output_path}")

    print(f"\nGenerated {generated} country map reports in {base_dir}/")


if __name__ == "__main__":
    generate_reports()
