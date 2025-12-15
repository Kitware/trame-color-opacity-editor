import type { Vector2D, Vector4D, ColorNode, ColorOpacityNode, OpacityNode } from '@/types'
import type { RGBAColor } from '@colormap/core'

export function fractionToPixel(
  f: Vector2D,
  size: Vector2D,
  padding: Vector2D,
  contentSize: Vector2D,
): Vector2D {
  return [padding[0] + f[0] * contentSize[0], size[1] - padding[1] - f[1] * contentSize[1]]
}

export function pixelToFraction(
  p: Vector2D,
  size: Vector2D,
  padding: Vector2D,
  contentSize: Vector2D,
): Vector2D {
  return [(p[0] - padding[0]) / contentSize[0], (size[1] - padding[1] - p[1]) / contentSize[1]]
}

export function mouseToPixel(m: Vector2D, rect: DOMRect): Vector2D {
  return [m[0] - rect.left, m[1] - rect.top]
}

export function pickNodeOnCanvas(
  p: Vector2D,
  context: CanvasRenderingContext2D,
): { id: number; type: 'handle' | 'edge' } | null {
  const color = context.getImageData(p[0], p[1], 1, 1).data

  // the picking canvas is transparent anywhere but where the nodes are
  if (color[3] === 255) {
    return {
      id: color[1]!,
      type: color[0] == 0 ? 'handle' : 'edge',
    }
  }

  return null
}

export function getNodeBounds(nodeId: number, nodes: OpacityNode[], epsilon: number): Vector4D {
  if (nodeId == 0) {
    return [0, nodes[1]![0] - epsilon, 0, 1]
  } else if (nodeId >= nodes.length - 1) {
    return [nodes[nodeId - 1]![0] + epsilon, 1, 0, 1]
  } else {
    return [nodes[nodeId - 1]![0] + epsilon, nodes[nodeId + 1]![0] - epsilon, 0, 1]
  }
}

export function clampNodeToBounds(f: Vector2D, bounds: Vector4D): Vector2D {
  const clamped: Vector2D = [...f]

  if (clamped[0] < bounds[0]) {
    clamped[0] = bounds[0]
  }

  if (clamped[0] > bounds[1]) {
    clamped[0] = bounds[1]
  }

  if (clamped[1] < bounds[2]) {
    clamped[1] = bounds[2]
  }

  if (clamped[1] > bounds[3]) {
    clamped[1] = bounds[3]
  }

  return clamped
}

export function drawCanvasBackground(
  context: CanvasRenderingContext2D,
  size: Vector2D,
  padding: Vector2D,
  contentSize: Vector2D,
  shape: Vector2D[],
  nodes: ColorNode[] | ColorOpacityNode[],
) {
  context.clearRect(0, 0, size[0], size[1])

  if (shape.length < 2) {
    return
  }

  let p0 = fractionToPixel([0, 0], size, padding, contentSize)
  const p1 = fractionToPixel([1, 0], size, padding, contentSize)

  const grad = context.createLinearGradient(p0[0], p0[1], p1[0], p1[1])

  nodes.forEach((node: ColorNode | ColorOpacityNode) => {
    const [value, color] = node

    let v = value;
    if (v < 0) {
      v = 0;
    } else if (v > 1) {
      v = 1;
    }

    if (color.length === 4) {
      const [r, g, b, a] = color
      grad.addColorStop(v, `rgba(${r * 255}, ${g * 255}, ${b * 255}, ${a})`)
    } else {
      const [r, g, b] = color
      grad.addColorStop(v, `rgba(${r * 255}, ${g * 255}, ${b * 255}, 1)`)
    }
  })

  context.fillStyle = grad

  context.beginPath()

  p0 = fractionToPixel(shape[0]!, size, padding, contentSize)
  context.moveTo(p0[0], p0[1])

  for (let i = 1; i < shape.length; i++) {
    p0 = fractionToPixel(shape[i]!, size, padding, contentSize)
    context.lineTo(p0[0], p0[1])
  }

  context.fill()
  // context.closePath();
}

export function drawCanvasControls(
  context: CanvasRenderingContext2D,
  pickerContext: CanvasRenderingContext2D,
  size: Vector2D,
  padding: Vector2D,
  contentSize: Vector2D,
  nodes: OpacityNode[],
  radius: number,
  showLine: boolean,
  lineWidth: number,
  color: RGBAColor,
  borderColor: RGBAColor,
) {
  context.clearRect(0, 0, size[0], size[1])
  pickerContext.clearRect(0, 0, size[0], size[1])

  if (showLine && nodes.length > 1) {
    context.beginPath()

    pickerContext.lineWidth = radius * 3
    pickerContext.beginPath()

    const [x, y] = fractionToPixel(nodes[0]!, size, padding, contentSize)
    context.moveTo(x, y)
    pickerContext.moveTo(x, y)

    for (let i = 1; i < nodes.length; ++i) {
      const [x, y] = fractionToPixel(nodes[i]!, size, padding, contentSize)

      pickerContext.strokeStyle = `rgb(${1}, ${i - 1}, ${0})`

      context.lineTo(x, y)

      pickerContext.lineTo(x, y)
      pickerContext.stroke()
      pickerContext.beginPath()
      pickerContext.moveTo(x, y)
    }

    context.strokeStyle = `rgba(${borderColor[0]}, ${borderColor[1]}, ${borderColor[2]}, ${borderColor[3]})`
    context.lineWidth = lineWidth * 1 + 1
    context.stroke()
    context.strokeStyle = `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${color[3]})`
    context.lineWidth = lineWidth
    context.stroke()
  }

  context.fillStyle = `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${color[3]})`
  context.strokeStyle = `rgba(${borderColor[0]}, ${borderColor[1]}, ${borderColor[2]}, ${borderColor[3]})`
  context.lineWidth = 2
  for (let i = 0; i < nodes.length; ++i) {
    const [x, y] = fractionToPixel(nodes[i]!, size, padding, contentSize)
    context.beginPath()
    context.arc(x, y, radius, 0, 2 * Math.PI)
    context.fill()
    context.stroke()

    // Use unique color needed to build the color to node map
    pickerContext.fillStyle = `rgb(${0}, ${i}, ${i})`
    pickerContext.beginPath()
    pickerContext.arc(x, y, radius * 3, 0, 2 * Math.PI)
    pickerContext.fill()
  }
}
