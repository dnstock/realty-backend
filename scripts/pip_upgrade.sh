#!/bin/sh

# Check if requirements.txt exists
if [ ! -f requirements.txt ]; then
    echo "requirements.txt not found. Please make sure the file exists in the current directory."
    exit 1
fi

# Upgrade each package in requirements.txt
echo "Upgrading packages listed in requirements.txt..."
while IFS= read -r line; do
    package_name="${line%%==*}" # Extract the package name before '=='
    if [[ -n "$package_name" ]]; then
        echo "Upgrading $package_name..."
        pip install --upgrade "$package_name"
    fi
done < requirements.txt

# Freeze updated versions back into requirements.txt
echo "Freezing updated packages into requirements.txt..."
pip freeze > requirements.txt

echo "Upgrade complete. Updated requirements.txt file generated."
