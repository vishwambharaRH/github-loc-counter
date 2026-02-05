use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};
use serde::{Deserialize, Serialize};
use walkdir::WalkDir;

#[derive(Debug, Deserialize)]
struct Config {
    patterns: Patterns,
    languages: HashMap<String, Vec<String>>,
}

#[derive(Debug, Deserialize)]
struct Patterns {
    ignore_dirs: Vec<String>,
    ignore_files: Vec<String>,
}

#[derive(Debug, Serialize)]
struct LocResults {
    languages: HashMap<String, u64>,
}

fn load_config() -> Result<Config, Box<dyn std::error::Error>> {
    let config_path = Path::new("ignore_rules.toml");
    let config_str = fs::read_to_string(config_path)?;
    let config: Config = toml::from_str(&config_str)?;
    Ok(config)
}

fn should_ignore_dir(dir_name: &str, ignore_patterns: &[String]) -> bool {
    ignore_patterns.iter().any(|pattern| dir_name == pattern)
}

fn should_ignore_file(file_name: &str, ignore_patterns: &[String]) -> bool {
    ignore_patterns.iter().any(|pattern| {
        if pattern.contains('*') {
            // Simple wildcard matching
            let pattern = pattern.trim_start_matches('*');
            file_name.ends_with(pattern)
        } else {
            file_name == pattern
        }
    })
}

fn get_language_for_extension(
    ext: &str,
    languages: &HashMap<String, Vec<String>>,
) -> Option<String> {
    for (lang, extensions) in languages {
        if extensions.iter().any(|e| e == ext) {
            return Some(lang.clone());
        }
    }
    None
}

fn count_lines_in_file(path: &Path) -> Result<u64, std::io::Error> {
    let content = fs::read_to_string(path)?;
    let line_count = content.lines().count() as u64;
    Ok(line_count)
}

fn count_loc_in_directory(
    dir: &Path,
    config: &Config,
) -> HashMap<String, u64> {
    let mut results: HashMap<String, u64> = HashMap::new();

    for entry in WalkDir::new(dir)
        .into_iter()
        .filter_entry(|e| {
            if e.file_type().is_dir() {
                let dir_name = e.file_name().to_string_lossy();
                !should_ignore_dir(&dir_name, &config.patterns.ignore_dirs)
            } else {
                true
            }
        })
    {
        let entry = match entry {
            Ok(e) => e,
            Err(_) => continue,
        };

        if !entry.file_type().is_file() {
            continue;
        }

        let file_name = entry.file_name().to_string_lossy();
        
        // Check if file should be ignored
        if should_ignore_file(&file_name, &config.patterns.ignore_files) {
            continue;
        }

        // Get file extension
        let extension = match entry.path().extension() {
            Some(ext) => format!(".{}", ext.to_string_lossy()),
            None => continue,
        };

        // Determine language
        let language = match get_language_for_extension(&extension, &config.languages) {
            Some(lang) => lang,
            None => continue,
        };

        // Count lines
        match count_lines_in_file(entry.path()) {
            Ok(lines) => {
                *results.entry(language).or_insert(0) += lines;
            }
            Err(_) => continue,
        }
    }

    results
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    
    if args.len() < 2 {
        eprintln!("Usage: {} <directory>", args[0]);
        std::process::exit(1);
    }

    let target_dir = Path::new(&args[1]);
    
    if !target_dir.exists() {
        eprintln!("Directory does not exist: {}", target_dir.display());
        std::process::exit(1);
    }

    let config = match load_config() {
        Ok(c) => c,
        Err(e) => {
            eprintln!("Error loading config: {}", e);
            std::process::exit(1);
        }
    };

    let mut total_results: HashMap<String, u64> = HashMap::new();

    // If the target is a directory containing multiple repos
    for entry in fs::read_dir(target_dir).unwrap() {
        let entry = entry.unwrap();
        let path = entry.path();
        
        if path.is_dir() {
            let repo_results = count_loc_in_directory(&path, &config);
            
            for (lang, count) in repo_results {
                *total_results.entry(lang).or_insert(0) += count;
            }
        }
    }

    // Output as JSON
    let output = serde_json::to_string(&total_results).unwrap();
    println!("{}", output);
}