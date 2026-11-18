from scripts.generate_index import load_games
from scripts.rule_paths import rule_path, title_folder


def test_title_folders_and_lookup(tmp_path):
    rules = tmp_path / "rules"
    assert title_folder("Arcs") == "A"
    assert title_folder("  7 Wonders") == "0-9"

    path = rule_path(rules, "7-wonders", "7 Wonders")
    path.parent.mkdir(parents=True)
    path.write_text('---\ntitle: "7 Wonders"\n---\n')

    assert path == rules / "0-9" / "7-wonders.md"
    assert rule_path(rules, "7-wonders") == path
    assert load_games(rules)[0]["slug"] == "7-wonders"
