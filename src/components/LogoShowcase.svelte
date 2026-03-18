<script lang="ts">
  import PixelLogo from "./PixelLogo.svelte";
  import { toroShape, brandScheme, eyeIndices, buildGroups } from "../lib/logos";
</script>

<div class="showcase">
  <PixelLogo rects={toroShape} scheme={brandScheme} {eyeIndices} {buildGroups} size={128} />
</div>

<style>
  .showcase {
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
