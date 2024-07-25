# Define source and destination directories
src_dir="aplquest"
dest_dir="mkdown"

# Move files from source to destination
for year in {2013..2023}; do
    if [ -d "${src_dir}/${year}" ]; then
        mv ${src_dir}/${year}/* ${dest_dir}/${year}/
    fi
done

