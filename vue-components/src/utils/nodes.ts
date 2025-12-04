import type { MapNode as ExtMapNode } from '@colormap/core/dist/types';

import type { MapNode, ColorNode, OpacityNode, Vector2D, RGBColor } from '@/types';

export class MapNodeAdapter<T> implements ExtMapNode<T> {
    _node: MapNode<T>;

    constructor(node: MapNode<T>) {
        this._node = node;
    }

    get value() {
        return this._node[0];
    }

    get mapped() {
        return this._node[1];
    }
}

export function isOpacityNode(node: MapNode<unknown> | undefined): node is OpacityNode {
    return Array.isArray(node) && typeof node[1] === 'number';
}

export function isColorNode(node: MapNode<unknown> | undefined): node is ColorNode {
    return Array.isArray(node) && Array.isArray(node[1]);
}

export function isOpacityNodes(nodes: MapNode<unknown>[]): nodes is OpacityNode[] {
    return isOpacityNode(nodes[0]);
}

export function isColorNodes(nodes: MapNode<unknown>[]): nodes is ColorNode[] {
    return isColorNode(nodes[0]);
}

function _scaleNodeX<T>(node: MapNode<T>, start: number, span: number): MapNode<T> {
    return [(node[0] - start) / span, node[1]];
}

function _unscaleNodeX<T>(node: MapNode<T>, start: number, span: number): MapNode<T> {
    return [start + node[0] * span, node[1]];
}

function _scaleNodeY(node: OpacityNode, start: number, span: number): OpacityNode {
    return [node[0], (node[1] - start) / span];
}

function _unscaleNodeY(node: OpacityNode, start: number, span: number): OpacityNode {
    return [node[0], start + node[1] * span];
}

export function scaleNodeX<T>(node: MapNode<T>, range: Vector2D): MapNode<T> {
    let span = Math.abs(range[1] - range[0]);
    return _scaleNodeX(node, range[0], span);
}

export function unscaleNodeX<T>(node: MapNode<T>, range: Vector2D): MapNode<T> {
    let span = Math.abs(range[1] - range[0]);
    return _unscaleNodeX(node, range[0], span);
}

export function scaleNodesX<T>(nodes: MapNode<T>[], range: Vector2D): MapNode<T>[] {
    let span = Math.abs(range[1] - range[0]);
    return nodes.map((node) => _scaleNodeX(node, range[0], span));
}

export function unscaleNodesX<T>(nodes: MapNode<T>[], range: Vector2D): MapNode<T>[] {
    let span = Math.abs(range[1] - range[0]);
    return nodes.map((node) => _unscaleNodeX(node, range[0], span));
}

export function scaleNodeY(node: OpacityNode, range: Vector2D): OpacityNode {
    let span = Math.abs(range[1] - range[0]);
    return _scaleNodeY(node, range[0], span);
}

export function unscaleNodeY(node: OpacityNode, range: Vector2D): OpacityNode {
    let span = Math.abs(range[1] - range[0]);
    return _unscaleNodeY(node, range[0], span);
}

export function scaleNodesY(nodes: OpacityNode[], range: Vector2D): OpacityNode[] {
    let span = Math.abs(range[1] - range[0]);
    return nodes.map((node) => _scaleNodeY(node, range[0], span));
}

export function unscaleNodesY(nodes: OpacityNode[], range: Vector2D): OpacityNode[] {
    let span = Math.abs(range[1] - range[0]);
    return nodes.map((node) => _unscaleNodeY(node, range[0], span));
}

export function scaleNodes<T>(nodes: MapNode<T>[], xRange?: Vector2D, yRange?: Vector2D): MapNode<T>[] {
    const scaleX = xRange != undefined;
    const scaleY = yRange != undefined;

    if (nodes.length == 0 || (!scaleX && !scaleY)) {
        return [...nodes];
    }

    if (isOpacityNodes(nodes)) {
        if (scaleX) {
            nodes = scaleNodesX(nodes, xRange) as MapNode<T>[];
        }

        if (scaleY) {
            nodes = scaleNodesY(nodes as OpacityNode[], yRange) as MapNode<T>[];
        }
    } else {
        if (scaleX) {
            nodes = scaleNodesX(nodes, xRange);
        }
    }

    return nodes;
}

export function unscaleNodes<T>(nodes: MapNode<T>[], xRange?: Vector2D, yRange?: Vector2D): MapNode<T>[] {
    const scaleX = xRange != undefined;
    const scaleY = yRange != undefined;

    if (nodes.length == 0 || (!scaleX && !scaleY)) {
        return [...nodes];
    }

    if (isOpacityNodes(nodes)) {
        if (scaleX) {
            nodes = unscaleNodesX(nodes, xRange) as MapNode<T>[];
        }

        if (scaleY) {
            nodes = unscaleNodesY(nodes as OpacityNode[], yRange) as MapNode<T>[];
        }
    } else {
        if (scaleX) {
            nodes = unscaleNodesX(nodes, xRange);
        }
    }

    return nodes;
}

export function unscaleNode<T>(node: MapNode<T>, xRange?: Vector2D, yRange?: Vector2D): MapNode<T> {
    const scaleX = xRange != undefined;
    const scaleY = yRange != undefined;

    if (!scaleX && !scaleY) {
        return [...node];
    }

    if (isOpacityNode(node)) {
        if (scaleX) {
            node = unscaleNodeX(node, xRange);
        }

        if (scaleY) {
            node = unscaleNodeY(node as OpacityNode, yRange) as MapNode<T>;
        }
    } else {
        if (scaleX) {
            node = unscaleNodeX(node, xRange);
        }
    }

    return node;
}
