"""
NexusAgent CLI Runner
Run autonomous deep research workflows directly from your terminal.
"""

import argparse
import sys
import os
import time

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from core.agent import NexusAgent, AgentConfig, StepTrace

def print_banner():
    banner = r"""
  _   _                      _                    _   
 | \ | | _____  ___   _ ___ / \   __ _  ___ _ __ | |_ 
 |  \| |/ _ \ \/ / | | / __/ _ \ / _` |/ _ \ '_ \| __|
 | |\  |  __/>  <| |_| \__ / ___ \ (_| |  __/ | | | |_ 
 |_| \_|\___/_/\_\\__,_|___/_/   \_\__, |\___|_| |_|\__|
                                   |___/                
       Autonomous Deep Research & Task Execution Agent
    """
    print(banner)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="NexusAgent: Autonomous Deep Research Agent")
    parser.add_argument(
        "--goal",
        "-g",
        type=str,
        default="State of Autonomous AI Agents and Multi-Tool Orchestration",
        help="The objective or research topic for the agent"
    )
    parser.add_argument(
        "--steps",
        "-s",
        type=int,
        default=4,
        help="Maximum ReAct steps (default: 4)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Optional path to save final Markdown report"
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["auto", "gemini", "simulation"],
        default="auto",
        help="Agent mode: auto (uses Gemini if API key found), gemini, or simulation"
    )

    args = parser.parse_args()

    print(f"[+] Initializing NexusAgent...")
    print(f"[+] Objective: {args.goal}")
    print(f"[+] Maximum Steps: {args.steps}")
    print(f"[+] Mode: {args.mode}")
    print("-" * 65)

    def on_step(trace: StepTrace):
        print(f"\n[Step {trace.step_number}]")
        print(f"  * Thought:    {trace.thought}")
        print(f"  * Tool Call:  {trace.tool_name}({trace.tool_input})")
        obs_preview = trace.observation.splitlines()[0] if trace.observation else ""
        if len(obs_preview) > 100:
            obs_preview = obs_preview[:100] + "..."
        print(f"  * Observation:{obs_preview}")
        if trace.reflection:
            print(f"  * Reflection: {trace.reflection}")

    config = AgentConfig(max_steps=args.steps, mode=args.mode)
    agent = NexusAgent(config=config)

    print("[*] Formulating dynamic execution plan...")
    response = agent.run(args.goal, on_step_callback=on_step)

    print("\n" + "=" * 65)
    print(f"[OK] Execution Complete in {response.duration_seconds}s via [{response.mode_used}]")
    print("=" * 65 + "\n")
    print(response.final_report)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(response.final_report)
        print(f"\n[OK] Report saved to: {args.output}")

if __name__ == "__main__":
    main()
