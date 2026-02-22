import kagglehub

# Download latest version
path = kagglehub.dataset_download("asaniczka/trending-youtube-videos-113-countries")

print("Path to dataset files:", path)
