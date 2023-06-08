from django import template


register = template.Library()

UNACCEPTABLE_WORDS = ['дурак', 'мудило', 'задница', 'сиськи']

@register.filter()
def censor(value):
   """
   value: значение, к которому нужно применить фильтр

   """
   value = [x for x in value.split(" ") if x]

   # for i, word in enumerate(value):
   #    if word.lower() in UNACCEPTABLE_WORDS:
   #       value[i] = f"{word[0]}{(len(word)-2) * '*'}{word[-1]}"


   cen_sor = ' '.join([
      f"{word[0]}{(len(word)-2) * '*'}{word[-1]}" if word.lower() in UNACCEPTABLE_WORDS else value[i]
      for i, word in enumerate(value)
   ])

   return cen_sor