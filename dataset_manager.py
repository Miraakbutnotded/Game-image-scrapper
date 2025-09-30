#!/usr/bin/env python3
"""
Dataset Manager - Handles dataset organization and metadata management
"""

import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional
import hashlib


class DatasetManager:
    """Manages dataset organization, metadata, and file operations"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.metadata_file = os.path.join(base_dir, "metadata.json")
        self.directories = {
            'videos': 'downloads',
            'video_frames': 'dataset', 
            'web_images': 'web_images',
            'real_images': 'real_images'
        }
        
        # Create all necessary directories
        for dir_path in self.directories.values():
            os.makedirs(os.path.join(base_dir, dir_path), exist_ok=True)
    
    def get_directory(self, dir_type: str) -> str:
        """Get full path for a directory type."""
        if dir_type in self.directories:
            return os.path.join(self.base_dir, self.directories[dir_type])
        return os.path.join(self.base_dir, dir_type)
    
    def organize_files(self, source_dir: str, target_type: str) -> int:
        """Move files from source to appropriate target directory."""
        source_path = os.path.join(self.base_dir, source_dir)
        target_path = self.get_directory(target_type)
        
        if not os.path.exists(source_path):
            return 0
        
        moved_count = 0
        for filename in os.listdir(source_path):
            source_file = os.path.join(source_path, filename)
            target_file = os.path.join(target_path, filename)
            
            if os.path.isfile(source_file):
                try:
                    os.rename(source_file, target_file)
                    moved_count += 1
                except OSError as e:
                    print(f"Error moving {filename}: {e}")
        
        return moved_count
    
    def get_file_stats(self) -> Dict[str, int]:
        """Get statistics about files in each directory."""
        stats = {}
        for dir_type, dir_name in self.directories.items():
            dir_path = os.path.join(self.base_dir, dir_name)
            if os.path.exists(dir_path):
                files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
                stats[dir_type] = len(files)
            else:
                stats[dir_type] = 0
        return stats
    
    def create_metadata_entry(self, file_path: str, source_type: str, source_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create a metadata entry for a file."""
        file_stats = os.stat(file_path)
        file_hash = self._calculate_file_hash(file_path)
        
        return {
            'filename': os.path.basename(file_path),
            'filepath': file_path,
            'source_type': source_type,  # 'youtube_video', 'youtube_frame', 'web_gallery', 'google_images'
            'source_info': source_info,
            'file_size': file_stats.st_size,
            'created_at': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            'modified_at': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            'file_hash': file_hash,
            'added_to_dataset': datetime.now().isoformat()
        }
    
    def save_metadata(self, metadata_entries: List[Dict[str, Any]]) -> None:
        """Save metadata entries to JSON file."""
        existing_metadata = self.load_metadata()
        
        # Add new entries (avoid duplicates based on file hash)
        existing_hashes = {entry.get('file_hash') for entry in existing_metadata}
        
        for entry in metadata_entries:
            if entry.get('file_hash') not in existing_hashes:
                existing_metadata.append(entry)
        
        with open(self.metadata_file, 'w') as f:
            json.dump(existing_metadata, f, indent=2)
    
    def load_metadata(self) -> List[Dict[str, Any]]:
        """Load existing metadata from JSON file."""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def export_metadata_csv(self, output_file: str = None) -> str:
        """Export metadata to CSV format."""
        if output_file is None:
            output_file = os.path.join(self.base_dir, "dataset_metadata.csv")
        
        metadata = self.load_metadata()
        
        if not metadata:
            print("No metadata to export")
            return output_file
        
        # Flatten nested dictionaries for CSV
        fieldnames = set()
        flattened_data = []
        
        for entry in metadata:
            flattened = {}
            for key, value in entry.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        flattened[f"{key}_{sub_key}"] = sub_value
                else:
                    flattened[key] = value
            flattened_data.append(flattened)
            fieldnames.update(flattened.keys())
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
            writer.writeheader()
            writer.writerows(flattened_data)
        
        print(f"Metadata exported to: {output_file}")
        return output_file
    
    def find_duplicates(self) -> List[List[Dict[str, Any]]]:
        """Find duplicate files based on file hash."""
        metadata = self.load_metadata()
        hash_groups = {}
        
        for entry in metadata:
            file_hash = entry.get('file_hash')
            if file_hash:
                if file_hash not in hash_groups:
                    hash_groups[file_hash] = []
                hash_groups[file_hash].append(entry)
        
        # Return groups with more than one file
        return [group for group in hash_groups.values() if len(group) > 1]
    
    def cleanup_broken_links(self) -> int:
        """Remove metadata entries for files that no longer exist."""
        metadata = self.load_metadata()
        valid_entries = []
        removed_count = 0
        
        for entry in metadata:
            filepath = entry.get('filepath')
            if filepath and os.path.exists(filepath):
                valid_entries.append(entry)
            else:
                removed_count += 1
        
        if removed_count > 0:
            with open(self.metadata_file, 'w') as f:
                json.dump(valid_entries, f, indent=2)
            print(f"Removed {removed_count} broken metadata entries")
        
        return removed_count
    
    def get_summary_report(self) -> Dict[str, Any]:
        """Generate a comprehensive summary report."""
        stats = self.get_file_stats()
        metadata = self.load_metadata()
        duplicates = self.find_duplicates()
        
        source_types = {}
        for entry in metadata:
            source_type = entry.get('source_type', 'unknown')
            source_types[source_type] = source_types.get(source_type, 0) + 1
        
        return {
            'file_counts': stats,
            'total_files': sum(stats.values()),
            'metadata_entries': len(metadata),
            'source_breakdown': source_types,
            'duplicate_groups': len(duplicates),
            'total_duplicates': sum(len(group) - 1 for group in duplicates),
            'last_updated': datetime.now().isoformat()
        }
    
    def _calculate_file_hash(self, filepath: str) -> str:
        """Calculate SHA256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except IOError:
            return ""
    
    def print_summary(self) -> None:
        """Print a formatted summary of the dataset."""
        report = self.get_summary_report()
        
        print("\n📊 Dataset Summary Report")
        print("=" * 50)
        
        print(f"\n📁 File Counts:")
        for dir_type, count in report['file_counts'].items():
            print(f"   {dir_type.replace('_', ' ').title()}: {count} files")
        
        print(f"\n📈 Total Files: {report['total_files']}")
        print(f"📋 Metadata Entries: {report['metadata_entries']}")
        
        if report['source_breakdown']:
            print(f"\n🎯 Source Breakdown:")
            for source, count in report['source_breakdown'].items():
                print(f"   {source.replace('_', ' ').title()}: {count} files")
        
        if report['duplicate_groups'] > 0:
            print(f"\n⚠️  Duplicates Found:")
            print(f"   {report['duplicate_groups']} groups with {report['total_duplicates']} duplicate files")
        
        print(f"\n🕒 Last Updated: {report['last_updated']}")
        print("=" * 50)