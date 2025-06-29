<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  min: { type: Number, default: 0 },
  max: { type: Number, default: 100 },
  label: { type: String, required: true },
  modelValue: { type: Number, default: 0 } // For v-model binding
});
const emit = defineEmits(['update:modelValue']);

const angle = ref(0);
const isDragging = ref(false);
const knobRef = ref(null);
const value = ref(props.modelValue);

// Convert value to angle
const valueToAngle = (val) => ((val - props.min) / (props.max - props.min)) * 270 - 135;

// Convert angle to value
const angleToValue = (angle) => {
  let val = ((angle + 135) / 270) * (props.max - props.min) + props.min;
  return Math.min(props.max, Math.max(props.min, val));
};

watch(() => props.modelValue, (val) => {
  angle.value = valueToAngle(val);
}, { immediate: true });

function startDrag(e) {
  isDragging.value = true;
  window.addEventListener('mousemove', onDrag);
  window.addEventListener('mouseup', stopDrag);
}

function onDrag(e) {
  if (!isDragging.value) return;

  const rect = knobRef.value.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;

  const dx = e.clientX - centerX;
  const dy = e.clientY - centerY;

  let angleDeg = Math.atan2(dy, dx) * 180 / Math.PI;
  angleDeg -= 90;
  if (angleDeg < -135) angleDeg = -135;
  if (angleDeg > 135) angleDeg = 135;

  angle.value = angleDeg;
  const newValue = Math.round(angleToValue(angleDeg));
  value.value = newValue;
  emit('update:modelValue', newValue);
}

function stopDrag() {
  isDragging.value = false;
  window.removeEventListener('mousemove', onDrag);
  window.removeEventListener('mouseup', stopDrag);
}

function increase() {
  value.value = (value.value +1) % props.max;
}

function decrease() {
  value.value = (value.value -1) % props.max;

  if (value.value < 0) value.value = props.max;
}

const rotationStyle = computed(() => ({
  transform: `rotate(${angle.value}deg)`
}));
</script>

<template>
  <div class="knob-wrapper">
    <div class="knob" ref="knobRef" :style="rotationStyle" @mousedown="startDrag"></div>
    <div class="knob-button-wrapper">
      <button class="knob-button" @click="increase">+</button>
      <button class="knob-button" @click="decrease">-</button>
    </div>

    <div class="knob-label">{{ label }}: {{ value }}</div>
  </div>
</template>

<style scoped>
.knob-wrapper {
  position: relative;
  display: flex;
  flex-direction: row;
  user-select: none;
}
.knob {
  width: 41px;
  height: 41px;
  background-color: #000;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #333;
  cursor: grab;
  transition: transform 0.1s linear;
}
.knob-label {
  position: absolute;
  color: #fff;
  font-family: Inter;
  font-size: 12px;
  font-weight: 400;
  top: 50px;
  width: 130%;
}

.knob-button {
  font-size: 20px;
  width: 16px;
  height: 16px;
  background: #eee;
  border: 1px solid #999;
  border-radius: 4px;
  cursor: pointer;
  user-select: none;
  display: flex;
  justify-content: center;
  align-items: center;
}
.knob-button:hover {
  background: #ddd;
}
.knob-button-wrapper {
  margin-top: 4px;
  margin-left: 2px;
}
</style>
