from PIL import Image, ImageDraw
import math, colorsys, random, json, openai
import quadTree as q

openai.api_key = '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'
length = 3840
n = 30
descSet = {'1'}

def createQuadTree():
    # x = numpy.random.rand(n) * length
    # y = numpy.random.rand(n) * length
    x = [random.uniform(750,length - 750) for _ in range(n)]
    y = [random.uniform(750,length - 750) for _ in range(n)]
    points = []
    for i in range(n):
        points.append(q.Point(x[i], y[i]))
    domain = q.Rect(q.Point(length/2, length/2), length/2, length/2)
    quad_tree = q.quadTree(domain)
    for p in points:
        quad_tree.insert(p)
    return quad_tree.pointList

def generateNft(numImages):
    print("Generating NFT Images")
    with open("imgs.json", "r") as file:
        data = json.load(file)
    f = open("colorNames.json")
    colorNamesData = json.load(f)
    count = 0
    while count < numImages:
        rand_color = random.uniform(0.0, 1.0)
        (r, g, b) = colorsys.hsv_to_rgb(rand_color, 0.65, 1.0)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        hex = '%02x%02x%02x' % (r, g, b)
        colorName = colorSearch(colorNamesData, hex, len(colorNamesData))
        if colorName not in data:
            qtp = createQuadTree() #quadTree points list
            image = Image.new('RGB', (length,length), (0,0,0))
            draw = ImageDraw.Draw(image)
            data[colorName] = { "Image number" : str(count)}
            string = '\\' + assignDescription(data, colorName)
            for j in range(n):
                rand_color += 0.005
                drawFractal(draw, qtp[j][0], qtp[j][1], random.randint(-360, 360), random.randint(10, 15), rand_color)
            image.resize((1080, 1080), Image.Resampling.LANCZOS)
            print(string)
            image.save(r"C:\Users\kusha\Desktop\reactweb\src\comps\Image generator\pngs" + string + '.png')
            count += 1
    f.close()
    with open("imgs.json", "w") as file:
        json.dump(data, file, indent= 4)
    print("Done")

def drawFractal(draw, x1, y1, angle, depth, color):
    if depth == 1:
        return
    branchLen = random.uniform(5.0, 8.0)
    x2 = x1 + int(math.cos(math.radians(angle)) * depth * branchLen)
    y2 = y1 + int(math.sin(math.radians(angle)) * depth * branchLen)
    (r, g, b) = colorsys.hsv_to_rgb(color, 0.65, 1.0)
    R, G, B = int(255 * r), int(255 * g), int(255 * b)
    hex = ('%02x%02x%02x' % (R, G, B))
    if depth > 12:
        draw.line([x1, y1, x2, y2], (R, G, B), 5)
    else:
        draw.line([x1, y1, x2, y2], (R, G, B), int(depth/1.5))

    drawFractal(draw, x2, y2, angle - 17, depth - 1, color)
    drawFractal(draw, x2, y2, angle + 17, depth - 1, color)

#Binary search to find specific color name 
def colorSearch(A, hex, n):
    target = int(hex, 16)
    L = 0
    R = n - 1
    while L <= R:
        M = (L + R) // 2
        decM = int(A[M][0], 16)
        if decM == target:
            return A[M][1]
        decPrev, decNext = int(A[M-1][0], 16), int(A[M+1][0], 16)
        if decPrev < target and target < decNext:
            return A[M][1]
        elif decM < target:
            L = M + 1
        else:
            R = M - 1

#Machine generated description for each image based on the color name
def assignDescription(data, color):
    response = openai.Completion.create(
    engine="text-curie-001",
    prompt=("Topic: Poetic titles of abstract artwork (painting and drawing) based on color:\nBlack Red Ochre Give love a chance\nPurple Deep Koamaru The silent void\nZest Bright Turquoise Lullaby\n" + color + ":"),
    temperature=0.9,
    max_tokens=20,
    top_p=1,
    frequency_penalty=0.8,
    presence_penalty=0.8
    )
    lines = (response['choices'][0]['text']).split('\n')
    line1 = lines[0].strip()
    if line1 not in descSet:
        descSet.add(line1)
        data[color]['Image Description'] = line1
    else:
        try:
            line2 = lines[1].strip()
            if line2 not in descSet:
                descSet.add(line2)
                data[color]['Image Description'] = line2
            else:
                data[color]['Image Description'] = color
        except:
                data[color]['Image Description'] = color
    return data[color]['Image Description']

if __name__ == '__main__':
    generateNft(50)
