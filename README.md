# Trash-E Smart Bin

**Name** OctoPi

**Product:** Trash-E Smart Bin

An autonomous, AI-driven smart bin that identifies waste with a camera and automatically opens the correct compartment: General Waste, Recycling or Compost. 

- [Watch the demo trailer](add LinkedIn link)
- [Project website](add website link) (a design mock-up of the product website, not connected to the bin)

## Team

| Name | Contributions |
|---|---|
| Oliver Flynn ([OliverJFlynn](https://github.com/OliverJFlynn)) | AI model, Raspberry Pi, building |
| Kudakwashe Chingwena | Design, Arduino, building |
| Sochikamma Umeigbo | Website design and creation, building |
| Abi-Gail Mesioye | Video trailer, building |

All four of us helped plan and build the bin.

## Product

Our product, Trash-E Smart Bin, is an autonomous, AI-driven smart bin designed to eliminate waste contamination at the source. It replaces passive, error-prone bins with an active sorting system.

The system operates on a hybrid computing architecture. When a user presents an item, a Raspberry Pi 5 utilises a camera and a YOLOv8 computer vision model to instantly identify the material. The Pi then signals an Arduino Mega, which drives high-torque servos to automatically open the correct compartment: General Waste, Recycling or Compost. If an item is unrecognised, an integrated barcode scanner acts as a seamless fallback.

```
Pi camera -> YOLOv8 on Raspberry Pi -> Arduino -> servos open the lid
```

Beyond accurate sorting, the bin has two further features:

- **Full-Level Detection:** sensors inside the compartments monitor how full each one is, when a lid is full rgb lights will go red and an alert will be on the screen.
- **7-Inch Touchscreen:** an interactive display mounted on the front of the unit that shows information (such as alerts) and the camera.

**Benefits**
- **Eliminates source contamination:** by removing the human decision-making process, it keeps recycling streams pure.
- **Reduced cognitive load:** users no longer have to read complex recycling labels or guess where an item goes. The bin makes the process frictionless.

The AI model, detection scripts and version history are in [`ai-model/`](ai-model/).

## Market

The UK waste management sector presents a significant opportunity for smart, AI-powered solutions. According to UK government statistics, total household waste reached approximately 25.9 million tonnes in 2023, and the national recycling rate remains relatively low at 44.6% (UK Government, 2024). Recycling rates across local authorities range from 15.8% to 62.9% (MRW, 2025).

**Competitive landscape.** The market is dominated by traditional collection systems and basic recycling bins, with limited integration of AI or automation. Emerging smart bins and IoT-based monitoring systems exist but often lack advanced real-time waste classification.

**Unique selling point.** Automated waste recognition and sorting, which removes the reliance on user knowledge. Unlike traditional bins, it actively improves recycling outcomes by ensuring correct disposal.

## Repository layout
```
ai-smart-bin/
├── README.md
├── ai-model/       YOLOv8 model, detection scripts and version history
├── hardware/       Components list [and Arduino code]
├── design/
│   ├── prototype/      Early design prototype the bin was based on
│   └── final-model/    3D models of the final bin
├── website/        [add if the files are available]
└── media/          Poster, QR code poster, logo and photos
```

## Tools
Python, C, Ultralytics YOLOv8, OpenCV, ONNX, Raspberry Pi, Arduino Mega, Blender, Figma, VS Code

## Limitations
- The project website is a mock-up and does not connect to the bin.
