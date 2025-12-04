import ColorOpacityEditor from "./ColorOpacityEditor.vue";
import NodeScaler from "./internal/NodeScaler.vue";
import ViewportContainer from "./internal/ViewportContainer.vue";
import BackgroundShaper from "./internal/BackgroundShaper.vue";
import BackgroundShaperFull from "./internal/BackgroundShaperFull.vue";
import BackgroundShaperOpacity from "./internal/BackgroundShaperOpacity.vue";
import BackgroundView from "./internal/BackgroundView.vue";
import ControlsView from "./internal/ControlsView.vue";
import BackgroundShaperHistograms from "./internal/BackgroundShaperHistograms.vue";
import NodeMerger from "./internal/NodeMerger.vue";
import NodeFlattener from "./internal/NodeFlattener.vue";

export default {
  trameCoeColorOpacityEditor: ColorOpacityEditor,
  trameCoeNodeScaler: NodeScaler,
  trameCoeNodeMerger: NodeMerger,
  trameCoeNodeFlattener: NodeFlattener,
  trameCoeViewportContainer: ViewportContainer,
  trameCoeBackgroundShaper: BackgroundShaper,
  trameCoeBackgroundShaperFull: BackgroundShaperFull,
  trameCoeBackgroundShaperOpacity: BackgroundShaperOpacity,
  trameCoeBackgroundShaperHistograms: BackgroundShaperHistograms,
  trameCoeBackgroundView: BackgroundView,
  trameCoeControlsView: ControlsView,
};
