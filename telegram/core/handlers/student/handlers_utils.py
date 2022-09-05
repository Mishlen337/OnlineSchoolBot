
def formatting(string: str) -> str:
    state, change = map(str, string.split(':'))
    return state + ': ' + '<b>' + change + '</b>' + '\n'