# React Version of IntroML App

This is a React version of the Gradio app, built with Vite.

## Features

- 4 inputs on the left side (input0, input1, input2, input3) with +/- buttons
- 3 weight groups in the center orange box, each with 4 weights
- Big +/- buttons on the right of each weight group for bulk updates
- 3 outputs on the right side showing calculated results
- Real-time calculation: `output = input0 * weight0 + input1 * weight1 + input2 * weight2 + input3 * weight3`

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

This will start the development server, typically at `http://localhost:5173`

## Build

```bash
npm run build
```

## Preview Production Build

```bash
npm run preview
```

## How It Works

- **Inputs**: Range from 0 to 1 (clamped)
- **Weights**: Range from -3 to 3 (clamped)
- **Outputs**: Calculated in real-time based on current input and weight values
- **Bulk Updates**: The big buttons update all weights in a group by adding/subtracting the corresponding input values
