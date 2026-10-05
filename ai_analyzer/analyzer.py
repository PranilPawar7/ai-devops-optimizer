import os
import re
from google import genai


def analyze_pipeline_log(log_text):
    findings = []

    if re.search(r"FAILED", log_text, re.IGNORECASE):
        findings.append({
            "type": "Test Failure",
            "severity": "High",
            "recommendation": "Inspect failed automated tests before deployment."
        })

    if "legacy builder is deprecated" in log_text.lower():
        findings.append({
            "type": "Docker Optimization",
            "severity": "Medium",
            "recommendation": "Use Docker BuildKit/buildx instead of the legacy Docker builder."
        })

    checkout_count = len(
        re.findall(
            r"\{\s*\((?:Declarative:\s*)?Checkout(?:\s+SCM)?\)",
            log_text,
            re.IGNORECASE
        )
    )

    if checkout_count > 1:
        findings.append({
            "type": "Pipeline Optimization",
            "severity": "Low",
            "recommendation": "Avoid duplicate Git checkout operations in the Jenkins pipeline."
        })

    if "pip as the 'root' user" in log_text.lower():
        findings.append({
            "type": "Environment Warning",
            "severity": "Low",
            "recommendation": "Use an isolated Python environment inside the Docker build."
        })

    if not findings:
        findings.append({
            "type": "No Major Issues",
            "severity": "Low",
            "recommendation": "Pipeline appears healthy. Continue monitoring execution time and resource usage."
        })

    return findings


def generate_ai_analysis(log_text, findings):

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is not configured. Rule-based analysis is available."

    client = genai.Client(api_key=api_key)

    findings_text = "\n".join(
        f"- {item['type']} | Severity: {item['severity']} | "
        f"Recommendation: {item['recommendation']}"
        for item in findings
    )

    prompt = f"""
You are an AI DevOps optimization assistant.

Analyze the Jenkins pipeline information below.

Detected findings:
{findings_text}

Jenkins pipeline log:
{log_text}

Provide:

AI DEVOPS ANALYSIS
==================

Pipeline Assessment:
Give a short assessment of the pipeline.

Issue Analysis:
Explain the important issues and their possible impact.

Optimization Recommendations:
Give practical recommendations.

Priority:
State what should be fixed first and explain why.

Performance Metrics to Measure:
Suggest metrics such as pipeline execution time, stage duration,
Docker image size, CPU usage, memory usage, and test execution time.

Expected Benefit:
Explain the expected operational benefit without inventing numerical results.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:

        print("\n[WARNING] Gemini AI service is temporarily unavailable.")
        print("[WARNING] Continuing with rule-based DevOps analysis.\n")

        return (
            "Gemini AI service is temporarily unavailable.\n\n"
            "Fallback Analysis:\n"
            "The rule-based DevOps analyzer successfully processed "
            "the Jenkins pipeline log.\n\n"
            "Detected findings and recommendations can still be used "
            "for DevOps optimization."
        )


def print_report(findings, ai_analysis):

    print("\n" + "=" * 70)
    print("AI-ASSISTED DEVOPS PIPELINE ANALYSIS")
    print("=" * 70)

    print("\nRULE-BASED FINDINGS")
    print("-------------------")

    for index, finding in enumerate(findings, start=1):
        print(f"\nFinding {index}")
        print(f"Type           : {finding['type']}")
        print(f"Severity       : {finding['severity']}")
        print(f"Recommendation : {finding['recommendation']}")

    print("\n" + "=" * 70)
    print("GEMINI AI ANALYSIS")
    print("=" * 70)

    print(ai_analysis)

    print("\n" + "=" * 70)


if __name__ == "__main__":

    log_file = "logs/jenkins_build_3.log"

    if not os.path.exists(log_file):
        print(f"ERROR: Jenkins log not found: {log_file}")
        raise SystemExit(1)

    with open(log_file, "r", encoding="utf-8") as file:
        pipeline_log = file.read()

    findings = analyze_pipeline_log(pipeline_log)

    ai_analysis = generate_ai_analysis(
        pipeline_log,
        findings
    )

    print_report(
        findings,
        ai_analysis
    )
