<script lang="ts">
  import PixelLogo from "./PixelLogo.svelte";
  import { brandScheme } from "../lib/logos";
  import {
    portraitShape,
    portraitEyeIndices,
    portraitBuildGroups,
    PORTRAIT_VIEWBOX,
  } from "../lib/portrait_data";
</script>

<div class="showcase">
  <PixelLogo
    rects={portraitShape}
    scheme={brandScheme}
    eyeIndices={portraitEyeIndices}
    buildGroups={portraitBuildGroups}
    size={128}
    viewBox={PORTRAIT_VIEWBOX}
    groupGap={120}
    innerGap={8}
  />
</div>

<style>
  .showcase {
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
