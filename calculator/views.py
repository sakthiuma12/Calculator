import json
import re
from decimal import Decimal, InvalidOperation, localcontext
from operator import add, mul, sub, truediv

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Calculation


OPERATIONS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}
NUMBER_PATTERN = re.compile(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$')


def index(request):
    return render(
        request,
        'calculator/index.html',
        {'calculations': Calculation.objects.all()[:10]},
    )


def _parse_number(value):
    if (
        not isinstance(value, str)
        or len(value) > 32
        or not NUMBER_PATTERN.fullmatch(value)
    ):
        raise ValueError('Enter a valid number.')

    number = Decimal(value)
    if not number.is_finite():
        raise ValueError('Enter a finite number.')
    return number


def _format_number(value):
    formatted = format(value, 'f')
    if '.' in formatted:
        formatted = formatted.rstrip('0').rstrip('.')
    return '0' if formatted in ('', '-0') else formatted


@require_POST
def calculate(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Request body must be valid JSON.'}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({'error': 'Request body must be a JSON object.'}, status=400)

    operator = payload.get('operator')
    if not isinstance(operator, str) or operator not in OPERATIONS:
        return JsonResponse({'error': 'Choose a supported operator.'}, status=400)

    try:
        left = _parse_number(payload.get('left'))
        right = _parse_number(payload.get('right'))
    except (InvalidOperation, ValueError):
        return JsonResponse({'error': 'Enter valid numbers.'}, status=400)

    if operator == '/' and right == 0:
        return JsonResponse({'error': 'Cannot divide by zero.'}, status=400)

    try:
        with localcontext() as context:
            context.prec = 50
            result = OPERATIONS[operator](left, right)
    except InvalidOperation:
        return JsonResponse({'error': 'The result is outside the supported range.'}, status=400)

    left_text = _format_number(left)
    right_text = _format_number(right)
    result_text = _format_number(result)
    expression = f'{left_text} {operator} {right_text}'
    calculation = Calculation.objects.create(
        expression=expression,
        result=result_text,
    )

    return JsonResponse(
        {
            'expression': calculation.expression,
            'result': calculation.result,
        },
        status=201,
    )
