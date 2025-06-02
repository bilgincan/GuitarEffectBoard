<template>
  <div class="pedal-container">
    <div class="pedal-body">
      <div class="delay-knob">
        <Knob v-model="delay" :min="0" :max="100" label="Delay" />
      </div>

      <div class="freq-knob">
        <Knob v-model="frequency" :min="0" :max="100" label="Freq" />
      </div>

      <div class="input-line"></div>
      <div class="input-label">Input</div>

      <div class="output-line"></div>
      <div class="output-label">Output</div>

      <div class="pedal-name">cnblgn dynamics delay pedal</div>

      <div class="led-indicator"
           :class="[isPedalActive ? ledIndicatorActiveClass : ledIndicatorInactiveClass]"></div>
      <div class="foot-switch" @click="switchPedalActive()"></div>
    </div>
  </div>
</template>

<script setup>
// Component logic can be added here if needed
import {ref} from "vue";
import '@/assets/pedals/delay.css'
import Knob from "@/models/knobs/Knob.vue";

let isPedalActive = ref(false);
const ledIndicatorActiveClass = ref("led-indicator-color-active");
const ledIndicatorInactiveClass = ref("led-indicator-color-inactive");

function switchPedalActive() {
  isPedalActive.value = !isPedalActive.value;
}

</script>
