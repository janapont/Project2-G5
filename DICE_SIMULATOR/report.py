import os
from fpdf import FPDF
from DICE_SIMULATOR import statistics as stats
from DICE_SIMULATOR import plots


def generate_report(simulator, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    distribution_path = os.path.join(output_folder, "distribution.png")
    single_dice_path = os.path.join(output_folder, "single_dice.png")
    pairs_odds_path = os.path.join(output_folder, "pairs_odds.png")
    doubles_path = os.path.join(output_folder, "doubles.png")

    plots.plot_distribution(simulator, save_path=distribution_path)
    plots.plot_single_dice(simulator, save_path=single_dice_path)
    plots.plot_pairs_vs_odds(simulator, save_path=pairs_odds_path)
    plots.plot_doubles(simulator, save_path=doubles_path)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Dice Simulator Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Number of throws: {simulator.get_n_throws()}", ln=True)
    pdf.cell(0, 8, f"Number of dice: {simulator.get_n_dice()}", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Interpretation of the questions:", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6,
        "- Q3 ranges follow the project statement (1-6 for 1 die, 7-12 for 2 dice).\n"
        "- Doubles: both dice show the same number (only with 2 dice).\n"
        "- Pairs: results that are even numbers.\n"
        "- Odds: results that are odd numbers."
    )
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Results:", ln=True)
    pdf.set_font("Helvetica", "", 11)

    most, least = stats.most_and_least_frequent(simulator)
    pdf.cell(0, 6, f"Most frequent result: {most}", ln=True)
    pdf.cell(0, 6, f"Least frequent result: {least}", ln=True)

    avg, minimum, maximum = stats.average_min_max(simulator)
    pdf.cell(0, 6, f"Average: {avg:.2f}", ln=True)
    pdf.cell(0, 6, f"Min: {minimum}", ln=True)
    pdf.cell(0, 6, f"Max: {maximum}", ln=True)

    pdf.cell(0, 6, f"Pairs (even): {stats.percentage_of_pairs(simulator):.2f}%", ln=True)
    pdf.cell(0, 6, f"Odds: {stats.percentage_of_odds(simulator):.2f}%", ln=True)
    if simulator.get_n_dice() == 2:
        pdf.cell(0, 6, f"Doubles: {stats.percentage_of_doubles(simulator):.2f}%", ln=True)

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Empirical probabilities:", ln=True)
    pdf.set_font("Helvetica", "", 11)
    values, probabilities = stats.empirical_probabilities(simulator)
    for v, p in zip(values, probabilities):
        pdf.cell(0, 6, f"  Result {v}: {p * 100:.2f}%", ln=True)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Plots", ln=True, align="C")
    pdf.ln(5)

    pdf.image(distribution_path, w=170)
    pdf.ln(5)
    pdf.image(single_dice_path, w=170)

    pdf.add_page()
    pdf.image(pairs_odds_path, w=170)
    pdf.ln(5)
    if simulator.get_n_dice() == 2:
        pdf.image(doubles_path, w=170)

    pdf_path = os.path.join(output_folder, "report.pdf")
    pdf.output(pdf_path)
    return pdf_path