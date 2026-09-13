import json
import subprocess
import time

CATEGORIES = [
    # AI Characters & People
    "ai_boys", "ai_girls", "ai_cyberpunk_boy", "ai_cyberpunk_girl", "ai_anime_boy", "ai_anime_girl",
    "ai_monk", "ai_warrior", "ai_samurai", "ai_ninja", "ai_astronaut", "ai_king", "ai_queen",
    "ai_robot", "ai_android", "ai_cyborg", "ai_demon", "ai_angel", "ai_vampire", "ai_wizard",
    "ai_witch", "ai_viking", "ai_knight", "ai_pirate", "ai_detective", "ai_doctor", "ai_teacher",
    "ai_alien", "ai_greek_god", "ai_pharaoh", "ai_superhero", "ai_villain", "ai_baby", "ai_old_man",
    "ai_old_woman", "ai_soldier", "ai_gladiator", "ai_spartan", "ai_ghost", "ai_zombie",
    
    # Nature & Scenery AI
    "ai_mountain", "ai_forest", "ai_ocean", "ai_space", "ai_galaxy", "ai_waterfall", "ai_desert",
    "ai_volcano", "ai_jungle", "ai_cave", "ai_skyline", "ai_sunset", "ai_aurora", "ai_snow_mountain",
    "ai_island", "ai_river", "ai_clouds", "ai_underwater", "ai_storm", "ai_lightning",

    # AI Animals & Creatures
    "ai_cat", "ai_dog", "ai_lion", "ai_tiger", "ai_wolf", "ai_dragon", "ai_phoenix", "ai_eagle",
    "ai_bear", "ai_snake", "ai_horse", "ai_monkey", "ai_fox", "ai_owl", "ai_shark", "ai_whale",
    "ai_dinosaur", "ai_unicorn", "ai_griffin", "ai_monster",

    # Sci-Fi, Fantasy & Architecture
    "ai_futuristic_city", "ai_cyberpunk_city", "ai_fantasy_castle", "ai_space_station",
    "ai_alien_planet", "ai_sci_fi_lab", "ai_neon_street", "ai_flying_car", "ai_time_portal",
    "ai_underwater_city", "ai_steampunk_world", "ai_floating_island", "ai_ancient_temple",
    "ai_pyramids", "ai_abandoned_city", "ai_post_apocalypse", "ai_dystopia", "ai_utopia",
    "ai_magic_forest", "ai_haunted_house",

    # Art Styles & Conceptual AI
    "ai_3d_avatar", "ai_hyperrealistic", "ai_unreal_engine", "ai_pixar_style", "ai_ghibli_style",
    "ai_cinematic_short", "ai_dark_fantasy", "ai_synthwave", "ai_vaporwave", "ai_surrealism",
    "ai_concept_art", "ai_glitch_art", "ai_hologram", "ai_neon_art", "ai_claymation",
    "ai_papercraft", "ai_pixel_art", "ai_low_poly", "ai_abstract_art", "ai_fractal_art",

    # AI Gaming & Pop Culture
    "ai_minecraft", "ai_gta6", "ai_fortnite", "ai_elden_ring", "ai_cyberpunk2077", "ai_pokemon",
    "ai_dragon_ball", "ai_naruto", "ai_one_piece", "ai_attack_on_titan", "ai_demon_slayer",
    "ai_marvel", "ai_dc_comics", "ai_star_wars", "ai_lord_of_the_rings", "ai_harry_potter",
    "ai_matrix", "ai_avatar_pandora", "ai_transformers", "ai_godzilla",

    # Vehicles & Technology AI
    "ai_supercar", "ai_hypercar", "ai_concept_bike", "ai_spaceship", "ai_mecha", "ai_jet",
    "ai_ufo", "ai_drone", "ai_hoverboard", "ai_quantum_computer",

    # AI Shorts Content & Stories
    "ai_motivation", "ai_quotes", "ai_history_facts", "ai_space_facts", "ai_scary_stories",
    "ai_horror_shorts", "ai_life_hacks", "ai_future_technology", "ai_time_travel",
    "ai_mind_blowing_facts", "ai_fitness_motivation", "ai_workout", "ai_dance", "ai_fashion",
    "ai_model", "ai_fitness_model", "ai_cooking", "ai_recipes", "ai_asmr", "ai_satisfying",
    "ai_illusion", "ai_magic_trick", "ai_deepfake_news", "ai_funny_shorts", "ai_comedy",
    "ai_memes", "ai_viral_shorts", "ai_trending", "ai_nature_documentary", "ai_meditation"
]

LINKS_PER_CATEGORY = 10

def fetch_shorts_for_category(category, count=10):
    query_text = category.replace('_', ' ')
    search_query = f"ytsearch25:#shorts {query_text} AI video"
    
    cmd = [
        "yt-dlp",
        search_query,
        "--dump-json",
        "--flat-playlist",
        "--ignore-errors",
        "--no-warnings",
        "--extractor-args", "youtube:player_client=android,web"
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    results = []
    seen_ids = set()
    
    for line in process.stdout:
        line_str = line.strip()
        if not line_str:
            continue
        try:
            video_data = json.loads(line_str)
            video_id = video_data.get("id")
            title = video_data.get("title", "AI Shorts Video")
            
            if video_id and video_id not in seen_ids:
                seen_ids.add(video_id)
                results.append({
                    "title": title,
                    "url": f"https://www.youtube.com/shorts/{video_id}"
                })
                
                if len(results) >= count:
                    break
        except Exception:
            continue
            
    return results

def main():
    data = {"categories": {}}
    total_fetched = 0
    
    print(f"Fetching {len(CATEGORIES)} categories...")
    
    for idx, category in enumerate(CATEGORIES, 1):
        shorts = fetch_shorts_for_category(category, LINKS_PER_CATEGORY)
        data["categories"][category] = shorts
        total_fetched += len(shorts)
        print(f"[{idx}/{len(CATEGORIES)}] {category}: {len(shorts)} shorts")
        time.sleep(0.2)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE] Total links fetched: {total_fetched}")

if __name__ == "__main__":
    main()
