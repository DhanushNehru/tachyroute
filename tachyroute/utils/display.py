"""Pretty-printing utilities for tachyroute results using rich."""
from typing import Any, Dict

from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


def _confidence_bar(confidence: float, width: int = 20) -> Text:
    """Render a confidence score as an inline colored bar."""
    confidence = max(0.0, min(confidence, 1.0))
    filled = int(confidence * width)
    empty = width - filled

    if confidence >= 0.75:
        color = "green"
    elif confidence >= 0.4:
        color = "yellow"
    else:
        color = "red"

    bar = Text()
    bar.append("█" * filled, style=color)
    bar.append("░" * empty, style="dim")
    bar.append(f"  {confidence:.0%}", style=f"bold {color}")
    return bar


def print_result(question_key: str, result: Dict[str, Any]) -> None:
    """
    Pretty-print a single DecisionResult dict (as returned inside
    Router.predict()'s "answers" mapping) as a rich table.

    Args:
        question_key: the key this result was stored under in `answers`
        result: a dict matching DecisionResult's shape
            (answer, confidence, evidence, exit_layer)
    """
    answer = result.get("answer")
    confidence = result.get("confidence", 0.0)
    evidence = result.get("evidence") or []
    exit_layer = result.get("exit_layer")

    table = Table(
        title=f"[bold]{question_key}[/bold]",
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
    )
    table.add_column("Field", style="bold cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Answer", Text(str(answer), style="bold white"))
    table.add_row("Confidence", _confidence_bar(float(confidence)))

    if exit_layer is not None:
        table.add_row("Exit layer", Text(str(exit_layer), style="magenta"))

    if evidence:
        ev_text = Text()
        for i, span in enumerate(evidence):
            if i > 0:
                ev_text.append("\n")
            ev_text.append(f'"{span}"', style="italic yellow")
        table.add_row("Evidence", ev_text)
    else:
        table.add_row("Evidence", Text("—", style="dim"))

    console.print(table)


def print_results(response: Dict[str, Any]) -> None:
    """
    Pretty-print an entire Router.predict() response: every question
    in `answers`, followed by routing metadata.

    Args:
        response: the full dict returned by Router.predict()
            ({"answers": {...}, "routing": {...}})
    """
    answers = response.get("answers", {})
    routing = response.get("routing", {})

    for q_key, res in answers.items():
        print_result(q_key, res)

    if routing:
        model = routing.get("model", "?")
        latency = routing.get("latency_ms", 0.0)
        reason = routing.get("reason", "")
        console.print(
            f"\n[dim]Routed to[/dim] [bold]{model}[/bold] "
            f"[dim]in[/dim] {latency:.1f}ms\n[dim]{reason}[/dim]"
        )
