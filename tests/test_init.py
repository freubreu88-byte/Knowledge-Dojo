"""Test vault initialization."""



from vibe_dojo.config import Config


def test_vault_folders_created(tmp_path):
    """Test that init-vault creates all required folders."""
    from vibe_dojo.cli import init_vault

    # Call the function directly
    init_vault(tmp_path)

    # Check folders exist
    expected_folders = [
        "00_Inbox",
        "00_Inbox/_attachments",
        "01_Drills",
        "02_Practice_Logs",
        "10_Mastery",
        "90_Archive",
    ]

    for folder in expected_folders:
        assert (tmp_path / folder).exists()
        assert (tmp_path / folder).is_dir()


def test_config_created(tmp_path):
    """Test that config.yaml is created with defaults."""
    from vibe_dojo.cli import init_vault

    init_vault(tmp_path)

    config_file = tmp_path / "config.yaml"
    assert config_file.exists()

    # Load and verify config
    config = Config(tmp_path)
    assert config.config["llm"]["provider"] == "gemini"
    assert config.config["defaults"]["timebox_min"] == 10


def test_home_md_created(tmp_path):
    """Test that Home.md is created."""
    from vibe_dojo.cli import init_vault

    init_vault(tmp_path)

    home_file = tmp_path / "Home.md"
    assert home_file.exists()
    content = home_file.read_text(encoding="utf-8")
    assert "Vibe-Dojo" in content
    assert "Quick Start" in content
