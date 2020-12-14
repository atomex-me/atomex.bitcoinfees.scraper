while true; do
    echo "Started Crawling..."
    python main.py
    echo "Crawling ended! Renaming file..."
    mv output/items.json output/items_consistent.json
    sleep 30;
done