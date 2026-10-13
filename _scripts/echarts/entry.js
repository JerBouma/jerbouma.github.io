// The parts of ECharts the site's charts use (assets/js/ft-charts.js), bundled
// into one file instead of the full library: about half the size to download
// and parse. Rebuild with _scripts/echarts/build.sh after using a new series
// type or component in ft-charts.js.
import * as echarts from 'echarts/core';
import { LineChart, BarChart, ScatterChart, HeatmapChart, CustomChart } from 'echarts/charts';
import {
  GridComponent, TooltipComponent, LegendComponent, DataZoomComponent,
  VisualMapComponent, MarkLineComponent, AxisPointerComponent
} from 'echarts/components';
import { LabelLayout } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  LineChart, BarChart, ScatterChart, HeatmapChart, CustomChart,
  GridComponent, TooltipComponent, LegendComponent, DataZoomComponent,
  VisualMapComponent, MarkLineComponent, AxisPointerComponent,
  LabelLayout, CanvasRenderer
]);

window.echarts = echarts;
