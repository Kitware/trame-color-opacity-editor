export type Vector2D = [number, number];
export type Vector3D = [number, number, number];
export type Vector4D = [number, number, number, number];
export type RGBColor = Vector3D;
export type RGBAColor = Vector4D;

export type MapNode<T> = [number, T];
/**
 * A node representing a color value
 */
export type ColorNode = MapNode<RGBColor>;

/**
 * A node representing an opacity value
 */
export type OpacityNode = MapNode<number>;

/**
 * A node representing a color-opacity value
 */
export type ColorOpacityNode = MapNode<RGBAColor>;

/**
 * A point in 2D space
 */
export type Point = Vector2D;
