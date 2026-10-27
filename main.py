"""
Crypto Analysis — Agentic Pipeline
Orchestrates: Customer Communicator -> News Analyst -> Price Analyst -> Report Writer
"""
from rich.console import Console
from rich.markdown import Markdown

from agent.communicator import parse_user_request
from agent.news_analyst import analyze_news
from agent.price_analyst import analyze_price
from agent.report_writer import write_report

console = Console()


def run_pipeline(user_input: str) -> str:
    console.print("\n[bold cyan]Step 1/4[/bold cyan] Customer Communicator — parsing request...")
    request = parse_user_request(user_input)
    coin, days = request["coin"], request["days"]
    console.print(f"  -> coin=[bold]{coin}[/bold], days=[bold]{days}[/bold]")

    console.print("[bold cyan]Step 2/4[/bold cyan] News Analyst — fetching + summarizing news...")
    news_result = analyze_news(coin)

    console.print("[bold cyan]Step 3/4[/bold cyan] Price Analyst — fetching + analyzing prices...")
    price_result = analyze_price(coin, days=days)

    console.print("[bold cyan]Step 4/4[/bold cyan] Report Writer — synthesizing final report...\n")
    report = write_report(coin, price_result, news_result)

    return report


if __name__ == "__main__":
    console.print("[bold green]Crypto Analysis Agent System[/bold green]")
    console.print("Example queries: 'How is Bitcoin doing this month?', 'ETH trend last 7 days'\n")

    user_query = input("Enter your query: ").strip()
    if not user_query:
        user_query = "How is Bitcoin doing this month?"

    try:
        final_report = run_pipeline(user_query)
        console.print(Markdown(final_report))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")