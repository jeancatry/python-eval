from ruler import Ruler

def test_not_empty_line(line):

    """
    A method that returns True only if the line is not wholy filled of ' '.

    """

    res = False
    count = len(line) - 2
    while count > 0:
        if line[count - 1] != ' ':
            return True
        count -= 1
    return res

to_compare = []
with open('DATASET.txt') as f:
    for line in f:
        if test_not_empty_line(line): #We only keep the "written" lines.
            to_compare.append(line)
    if len(to_compare) % 2 == 1:  #we 'silently' get rid of the last line if the total is not even.
        to_compare.pop()
    for i in range(int(len(to_compare) / 2)):
        ruler = Ruler(to_compare[2 * i], to_compare[2 * i + 1])
        ruler.compute() 
        dist = ruler.distance
        top, bottom = ruler.report()
        print(f"== comparison # {i + 1} - distance = {dist}\n{top}\n{bottom}")


        