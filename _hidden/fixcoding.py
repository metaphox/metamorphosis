import re, codecs

prefix = '/Users/metaphox/Projects/metamorphosis/_posts/'
match = dict()

with codecs.open(prefix + 'toprocess', encoding = 'utf-8') as top, codecs.open(prefix + '/temp') as proper:
  for line in proper.readlines():    
    mall = re.findall(r'/post/(.+)">(.+?)<', line)
    if len(mall) > 0:
      k, v = mall[0]
      match[k] = v
    
  for line in top.readlines():
    line = line.strip(' \t\n\r')
    idt = line.split('-')[3].split('.')[0]
    remove_next_line = False
    with file(line, 'w') as to, file('/Users/metaphox/Projects/metamorphosis/_posts/' + line) as fromm:
      for each in fromm.readlines():
        if each.find('!binary') > -1:
          to.write('title: '+match[idt]+'\n')
          remove_next_line = True
        else :
          if remove_next_line:
            remove_next_line = False
            continue
          to.write(each)
          
  print match
    
    
