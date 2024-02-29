relevant_keywords = [
    "fast processor", "ample RAM", "comfortable keyboard", "screen size", "budget",
    "accurate color reproduction", "high resolution", "connectivity options",
    "wireless connectivity", "duplex printing", "inkjet/laser technology", "additional features",
    "waterproof", "long battery life", "GPS tracking", "heart rate monitoring",
    "durable", "parental controls", "access to educational apps", "operating system preference",
    "splash-proof design", "brand preference", "large buttons", "easy-to-use features",
    "active noise cancellation", "specific brands", "touch controls",
    "good image quality", "4K video recording", "interchangeable lenses", "accessories",
    "powerful hardware", "online multiplayer support", "specific gaming titles", "extra controllers",
    "fast Wi-Fi speeds", "strong signal coverage", "dual-band/tri-band", "parental controls",
    "accurate translation", "offline support", "handheld device", "smartphone app",
    "large storage capacity", "fast data transfer speeds", "connectivity options",
    "two-way audio", "motion detection", "treat dispenser", "smartphone app integration",
    "E Ink display", "adjustable font sizes", "built-in lighting",
    "energy efficiency", "display technology", "refresh rate", "HDR support",
    "smart features", "voice control", "remote control", "portability",
    "storage options", "expandable storage", "multi-tasking capabilities",
    "multimedia capabilities", "virtual assistant integration", "IoT compatibility",
    "smart home integration", "digital assistant compatibility", "voice recognition",
    "intuitive interface", "ergonomic design", "compact size", "lightweight",
    "heavy-duty construction", "user-friendly interface", "built-in camera",
    "built-in microphone", "voice commands", "gesture controls", "touchscreen display",
    "high-fidelity audio", "surround sound", "noise isolation", "battery backup",
    "wireless charging", "fast charging", "multi-device compatibility", "expandability",
    "longevity", "reliability", "warranty coverage", "environmental friendliness",
    "recyclability", "sustainability", "energy-saving features", "low power consumption"
]
with open("keywords.txt", "w") as file:
    for keyword in relevant_keywords:
        file.write(keyword + "\n")
