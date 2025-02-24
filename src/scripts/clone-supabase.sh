#!/bin/bash

if [ -d "./storage/supabase" ]; then
    echo "Supabase already exists"
    exit 0
fi

cd storage
git clone --depth 1 https://github.com/supabase/supabase
cd supabase/docker

cp .env.example .env

docker compose pull

echo "Supabase is running"
