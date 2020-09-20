import json
import codecs
import pdfx
from checkLinks import check_refs

# pdf = pdfx.PDFx("pdf/policy-118.pdf")


def processPDF(name, domain):
    """
    Takes a single PDF, checks its urls and saves the results to a file.
    Returns a list of PDFs from our domain that aren't 404ing
    """
    print("Inspecting ", name)
    pdf = pdfx.PDFx(name)
    allRefs = pdf.get_references()

    refs = [
        ref for ref in allRefs if ref.reftype in ["url", "pdf"]
    ]
    print("\nChecking %s URLs for broken links..." % len(refs))

    refChecks = check_refs(refs)
    pdf.summary['refCheck'] = refChecks

    # Remove unneeded attributes
    if ('xapmm' in pdf.summary['metadata']):
        del pdf.summary['metadata']['xapmm']
    if ('xap' in pdf.summary['metadata']):
        del pdf.summary['metadata']['xap']

    # Export results
    text = json.dumps(pdf.summary, indent=4)
    pdfName = pdf.summary["source"]["filename"].split(".")[0]
    fileName = "output/" + pdfName + ".json"
    with codecs.open(fileName, "w", "utf-8") as f:
        f.write(text)

    # Check for new PDFs to review.
    # Remove any that fail the 404 check
    otherPDFs = [
        ref.ref for ref in allRefs
        if ref.reftype == "pdf"
        and domain in ref.ref
        and ref.ref in refChecks["200"]
    ]
    return otherPDFs


domain = "port.ac.uk"
pdfsToProcess = set(["policy-118.pdf"])
processedPDFs = []

# Take a PDF, process it, mark it as done, save any new PDFs that haven't been processed
while pdfsToProcess:
    print("todo: ", len(pdfsToProcess))
    print("done: ", len(processedPDFs))
    currentPDF = pdfsToProcess.pop()
    pdfsToAdd = processPDF(currentPDF, domain)
    processedPDFs.append(currentPDF)
    newPDFs = [pdf for pdf in pdfsToAdd if pdf not in processedPDFs]
    for newPDF in newPDFs:
        pdfsToProcess.add(newPDF)
