const display = document.querySelector('#display');
const expressionDisplay = document.querySelector('#expression');
const errorDisplay = document.querySelector('#error');
const keypad = document.querySelector('#keypad');

let currentInput = '0';
let leftOperand = null;
let pendingOperator = null;
let shouldStartNewInput = false;

function render() {
    display.textContent = currentInput;
}

function clearError() {
    errorDisplay.textContent = '';
}

function enterDigit(digit) {
    clearError();
    if (shouldStartNewInput) {
        currentInput = digit;
        shouldStartNewInput = false;
    } else if (currentInput === '0') {
        currentInput = digit;
    } else if (currentInput.replace('-', '').length < 32) {
        currentInput += digit;
    }
    render();
}

function chooseOperator(operator) {
    clearError();
    leftOperand = currentInput;
    pendingOperator = operator;
    expressionDisplay.textContent = `${currentInput} ${operator}`;
    shouldStartNewInput = true;
}

function enterDecimal() {
    clearError();
    if (shouldStartNewInput) {
        currentInput = '0';
        shouldStartNewInput = false;
    }
    if (!currentInput.includes('.')) {
        currentInput += '.';
        render();
    }
}

function clearCalculator() {
    currentInput = '0';
    leftOperand = null;
    pendingOperator = null;
    shouldStartNewInput = false;
    expressionDisplay.textContent = 'Ready';
    clearError();
    render();
}

function deleteDigit() {
    clearError();
    currentInput = currentInput.length > 1 ? currentInput.slice(0, -1) : '0';
    if (currentInput === '-') currentInput = '0';
    shouldStartNewInput = false;
    render();
}

async function calculate() {
    if (leftOperand === null || pendingOperator === null || shouldStartNewInput) return;

    clearError();
    const operator = pendingOperator;
    const left = leftOperand;
    const right = currentInput;

    try {
        const response = await fetch('/calculate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ left, operator, right }),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Calculation failed.');

        expressionDisplay.textContent = data.expression;
        currentInput = data.result;
        leftOperand = null;
        pendingOperator = null;
        shouldStartNewInput = true;
        render();
        addHistoryItem(data.expression, data.result);
    } catch (error) {
        errorDisplay.textContent = error.message || 'Could not reach the calculator.';
    }
}

function addHistoryItem(expression, result) {
    const list = document.querySelector('#history-list');
    const emptyMessage = document.querySelector('#history-empty');
    if (emptyMessage) emptyMessage.remove();

    const item = document.createElement('li');
    item.className = 'history__item';

    const expressionText = document.createElement('span');
    expressionText.className = 'history__expression';
    expressionText.textContent = expression;

    const resultText = document.createElement('strong');
    resultText.textContent = result;

    item.append(expressionText, resultText);
    list.prepend(item);
    while (list.children.length > 10) list.lastElementChild.remove();

    document.querySelector('.history__count').textContent = list.children.length;
}

keypad.addEventListener('click', (event) => {
    const button = event.target.closest('button');
    if (!button) return;

    if (button.dataset.digit !== undefined) enterDigit(button.dataset.digit);
    else if (button.dataset.operator) chooseOperator(button.dataset.operator);
    else if (button.dataset.action === 'decimal') enterDecimal();
    else if (button.dataset.action === 'clear') clearCalculator();
    else if (button.dataset.action === 'delete') deleteDigit();
    else if (button.dataset.action === 'equals') calculate();
});
