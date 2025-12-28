# Collatz Multiverse: A Visualizer and Data Exporter
A professional-grade Python tool that explores the 3n + 1 problem, but with a twist of allowing users to replace the multiplier (3) and modifier (+1) with a number of their desires in the format *qn+r*. This application doesn't just calculate sequences; it provides a full suite for data analysis and visualization. 

---

#### Note: entered numbers lose precision as they become more unspeakably high

#### To test unspeakably high numbers accurately or see the Research behind this project: *[Click Here](https://github.com/saifkayyali3/Collatz_Research)*

---

## Features Special to this Collatz Visualizer version
- Allows users to enter any number they want to in $qn+r$ format

- Allows users to test negative numbers in their own $qn+r$ equation

- Limit of 10,000 steps of calculation and limit of `googol` digits of final number

---

## Features found in both [Collatz Standard](https://github.com/saifkayyali3/CollatzStandard) and Collatz Multiverse:
- Algorithmic Calculation: Fast processing of the Collatz sequence for any integer

- Interactive Visualization: Generates dynamic line graphs using Matplotlib to show the "hailstone" peaks and valleys.

- Data Export: Utilizes Pandas to serialize sequence data into a `.csv` file for external analysis in Excel or SQL.

- Adaptive Logarithmic Scaling: Automatically switches to $Log_{10}$ visualization for unspeakably high numbers to prevent hardware overflow and maintain graph readability.

---

## Technologies Used:
Programming Language: *Python*

Libraries Used: `Tkinter`, `Pandas` and `Matplolib`

Concepts: Data Engineering pipelines, State Management, Mathematical Modeling.

---

## How to Run:
Follow these steps to run the project locally:

### 1. Clone the repository and enter:
```bash
git clone https://github.com/saifkayyali3/Collatz-Multiverse.git
cd Collatz_Multiverse
```
### 2. Make a virtual environment
```bash
python -m venv venv

source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows
```

### 3. Install the needed requirements
```bash
pip install -r requirements.txt
```

### 4. Run
```bash
python Collatz_Multiverse.py

```
## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Author
**Saif Kayyali**