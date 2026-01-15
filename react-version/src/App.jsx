import React, { useState, useRef, useEffect } from 'react'
import './App.css'

function calculateResult(input0, input1, input2, input3, weight0, weight1, weight2, weight3) {
  return input0 * weight0 + input1 * weight1 + input2 * weight2 + input3 * weight3
}

function App() {
  // Weight limits (stored once)
  const MIN_WEIGHT = -9
  const MAX_WEIGHT = 9

  // Input states (clamped between 0 and 1)
  const [input0, setInput0] = useState(0)
  const [input1, setInput1] = useState(1)
  const [input2, setInput2] = useState(1)
  const [input3, setInput3] = useState(1)

  // Weight states (clamped between MIN_WEIGHT and MAX_WEIGHT)
  const [weights, setWeights] = useState([
    [0, 0, 0, 0], // Group 0
    [0, 0, 0, 0], // Group 1
    [0, 0, 0, 0], // Group 2
  ])
  const [isTraining, setIsTraining] = useState(false)

  // Calculate outputs
  const outputs = weights.map((groupWeights) =>
    calculateResult(input0, input1, input2, input3, ...groupWeights)
  )

  // Find highest output and check if there's a single maximum
  const maxValue = Math.max(...outputs)
  const maxIndices = outputs
    .map((val, idx) => (val === maxValue ? idx : -1))
    .filter((idx) => idx !== -1)
  const hasSingleMax = maxIndices.length === 1
  const maxIndex = hasSingleMax ? maxIndices[0] : -1

  // Labels for outputs
  const outputLabels = ['Wecker', 'Apfel', 'Hund']

  // Refs for input circles
  const inputRefs = [useRef(null), useRef(null), useRef(null), useRef(null)]
  
  // Refs for weight circles - 3 groups, 4 weights each
  const weightRefs = [
    [useRef(null), useRef(null), useRef(null), useRef(null)], // Group 0
    [useRef(null), useRef(null), useRef(null), useRef(null)], // Group 1
    [useRef(null), useRef(null), useRef(null), useRef(null)], // Group 2
  ]

  // Load training data values into inputs
  const loadTrainingData = (values) => {
    setInput0(Math.max(0, Math.min(1, values[0])))
    setInput1(Math.max(0, Math.min(1, values[1])))
    setInput2(Math.max(0, Math.min(1, values[2])))
    setInput3(Math.max(0, Math.min(1, values[3])))
  }

  // Training data values and labels
  const trainingData = [
    [1, 1, 0, 1],
    [1, 1, 1, 0],
    [1, 0, 1, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
  ]
  const trainingLabels = [0, 0, 1, 1, 2, 2]

  // Evaluate training data: calculate outputs and check if prediction matches label
  const evaluateTrainingData = (dataValues) => {
    const outputs = weights.map((groupWeights) =>
      calculateResult(dataValues[0], dataValues[1], dataValues[2], dataValues[3], ...groupWeights)
    )
    // Find maximum value
    const maxValue = Math.max(...outputs)
    // Find all indices with maximum value
    const maxIndices = outputs
      .map((val, idx) => (val === maxValue ? idx : -1))
      .filter((idx) => idx !== -1)
    
    // Check if there's a single maximum (not tied)
    if (maxIndices.length === 1) {
      return maxIndices[0]
    }
    // If there's a tie, return -1 to indicate no clear winner
    return -1
  }

  // Check if individual weight update would go out of bounds
  const canUpdateWeight = (groupIndex, weightIndex, delta) => {
    const currentWeight = weights[groupIndex][weightIndex]
    const newVal = currentWeight + delta
    return newVal >= MIN_WEIGHT && newVal <= MAX_WEIGHT
  }

  // Update single weight
  const updateWeight = (groupIndex, weightIndex, delta) => {
    if (!canUpdateWeight(groupIndex, weightIndex, delta)) return
    
    setWeights((prev) => {
      const newWeights = prev.map((group, gIdx) => {
        if (gIdx === groupIndex) {
          return group.map((w, wIdx) => {
            if (wIdx === weightIndex) {
              const newVal = w + delta
              return Math.max(MIN_WEIGHT, Math.min(MAX_WEIGHT, newVal))
            }
            return w
          })
        }
        return group
      })
      return newWeights
    })
  }

  // Check if bulk update would cause any weight to go out of bounds
  const canBulkUpdateWeights = (groupIndex, delta) => {
    const groupWeights = weights[groupIndex]
    const inputs = [input0, input1, input2, input3]
    
    for (let wIdx = 0; wIdx < groupWeights.length; wIdx++) {
      const currentWeight = groupWeights[wIdx]
      const newVal = currentWeight + delta * inputs[wIdx]
      if (newVal < MIN_WEIGHT || newVal > MAX_WEIGHT) {
        return false
      }
    }
    return true
  }

  // Bulk update all weights in a group
  const bulkUpdateWeights = (groupIndex, delta) => {
    if (!canBulkUpdateWeights(groupIndex, delta)) return
    
    setWeights((prev) => {
      const newWeights = prev.map((group, gIdx) => {
        if (gIdx === groupIndex) {
          return group.map((w, wIdx) => {
            const inputs = [input0, input1, input2, input3]
            const newVal = w + delta * inputs[wIdx]
            return Math.max(MIN_WEIGHT, Math.min(MAX_WEIGHT, newVal))
          })
        }
        return group
      })
      return newWeights
    })
  }

  // Reset all weights to 0
  const resetWeights = () => {
    setWeights([
      [0, 0, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0],
    ])
  }

  // Helper: apply bulk update to a copy of weights using given data values
  const applyBulkUpdateToWeights = (currentWeights, groupIndex, delta, dataValues) => {
    return currentWeights.map((group, gIdx) => {
      if (gIdx !== groupIndex) return group
      return group.map((w, wIdx) => {
        const newVal = w + delta * dataValues[wIdx]
        return Math.max(MIN_WEIGHT, Math.min(MAX_WEIGHT, newVal))
      })
    })
  }

  // Run simple ML training over the training data
  const runMLTraining = async () => {
    if (isTraining) return
    setIsTraining(true)

    let currentWeights = weights
    const epochs = 10

    const predictLabelForData = (weightsMatrix, dataValues) => {
      const outputsForData = weightsMatrix.map((groupWeights) =>
        calculateResult(
          dataValues[0],
          dataValues[1],
          dataValues[2],
          dataValues[3],
          ...groupWeights,
        ),
      )
      const maxVal = Math.max(...outputsForData)
      const maxIndices = outputsForData
        .map((val, idx) => (val === maxVal ? idx : -1))
        .filter((idx) => idx !== -1)
      if (maxIndices.length === 1) {
        return maxIndices[0]
      }
      return -1
    }

    for (let epoch = 0; epoch < epochs; epoch++) {
      for (let i = 0; i < trainingData.length; i++) {
        const dataValues = trainingData[i]
        const correctLabel = trainingLabels[i]

        // Mark current training data as loaded (like clicking it)
        setInput0(dataValues[0])
        setInput1(dataValues[1])
        setInput2(dataValues[2])
        setInput3(dataValues[3])

        const predicted = predictLabelForData(currentWeights, dataValues)

        if (predicted === correctLabel) {
          // do nothing
        } else {
          if (predicted !== -1) {
            // Wrong class: bulk dec for wrong class
            currentWeights = applyBulkUpdateToWeights(
              currentWeights,
              predicted,
              -1,
              dataValues,
            )
          }
          // Bulk inc for correct class
          currentWeights = applyBulkUpdateToWeights(
            currentWeights,
            correctLabel,
            1,
            dataValues,
          )
          setWeights(currentWeights)
        }

        // Wait half a second between steps
        // eslint-disable-next-line no-await-in-loop
        await new Promise((resolve) => setTimeout(resolve, 500))
      }
    }

    setIsTraining(false)
  }

  return (
    <div className="app">
      <div className="main-row">
        <ConnectionLines inputRefs={inputRefs} weightRefs={weightRefs} />
        {/* Left side - Inputs and Presets */}
        <div className="side-column left-column">
          <div className="left-side-container">
            {/* Training data boxes */}
            <div className="presets-container">
              {trainingData.map((dataValues, index) => {
                const predictedLabel = evaluateTrainingData(dataValues)
                const actualLabel = trainingLabels[index]
                // Correct only if there's a single maximum and it matches the label
                const isCorrect = predictedLabel !== -1 && predictedLabel === actualLabel
                // Check if this training data is currently loaded
                const isLoaded = input0 === dataValues[0] && 
                                input1 === dataValues[1] && 
                                input2 === dataValues[2] && 
                                input3 === dataValues[3]
                return (
                  <TrainingDataBox
                    key={index}
                    values={dataValues}
                    isCorrect={isCorrect}
                    isLoaded={isLoaded}
                    onClick={() => loadTrainingData(dataValues)}
                  />
                )
              })}
            </div>
            
            {/* Inputs */}
            <div className="inputs-container">
              <InputControl value={input0} ref={inputRefs[0]} />
              <InputControl value={input1} ref={inputRefs[1]} />
              <InputControl value={input2} ref={inputRefs[2]} />
              <InputControl value={input3} ref={inputRefs[3]} />
            </div>
          </div>
        </div>

        {/* Center - Orange box with weights */}
        <div className="center-column">
          <div className="orange-box">
            <button className="reset-btn" onClick={resetWeights} disabled={isTraining}>
              Reset
            </button>
            <button className="ml-btn" onClick={runMLTraining} disabled={isTraining}>
              ML
            </button>
            {weights.map((groupWeights, groupIndex) => (
              <WeightGroup
                key={groupIndex}
                weights={groupWeights}
                groupIndex={groupIndex}
                onWeightUpdate={updateWeight}
                onBulkDecrement={() => bulkUpdateWeights(groupIndex, -1)}
                onBulkIncrement={() => bulkUpdateWeights(groupIndex, 1)}
                canUpdateWeight={canUpdateWeight}
                canBulkUpdateWeights={canBulkUpdateWeights}
                weightRefs={weightRefs[groupIndex]}
              />
            ))}
          </div>
        </div>

        {/* Right side - Outputs */}
        <div className="side-column right-column">
          {outputs.map((output, index) => {
            const isHighest = output === maxValue
            return (
              <div key={index} className="output-container">
                <div 
                  className={`circle result-circle output-circle ${isHighest ? 'highest-output' : ''}`}
                >
                  {output}
                </div>
                <span className={`output-label ${isHighest ? 'highest-output' : ''}`}>
                  {outputLabels[index]}
                </span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

const InputControl = React.forwardRef(({ value }, ref) => {
  return (
    <div className="control-row input-control-row">
      <div ref={ref} className="circle input-circle">{value}</div>
    </div>
  )
})

function TrainingDataBox({ values, isCorrect, isLoaded, onClick }) {
  return (
    <div 
      className={`preset-box training-data-box ${isCorrect ? 'correct' : 'incorrect'} ${isLoaded ? 'loaded' : ''}`} 
      onClick={onClick}
    >
      {values.map((val, index) => (
        <span key={index} className="preset-value">
          {val}
        </span>
      ))}
    </div>
  )
}

function WeightGroup({ weights, groupIndex, onWeightUpdate, onBulkDecrement, onBulkIncrement, canUpdateWeight, canBulkUpdateWeights, weightRefs }) {
  return (
    <div className="control-group">
      <div className="big-buttons-row">
        <button 
          className="big-step-btn weight-big-btn" 
          onClick={onBulkIncrement}
          disabled={!canBulkUpdateWeights(groupIndex, 1)}
        >
          +
        </button>
        <button 
          className="big-step-btn weight-big-btn" 
          onClick={onBulkDecrement}
          disabled={!canBulkUpdateWeights(groupIndex, -1)}
        >
          −
        </button>
      </div>
      <div className="weight-controls">
        {weights.map((weight, weightIndex) => (
          <div key={weightIndex} className="control-row weight-control-row">
            <button
              className="step-btn weight-btn"
              onClick={() => onWeightUpdate(groupIndex, weightIndex, -1)}
              disabled={!canUpdateWeight(groupIndex, weightIndex, -1)}
              ref={weightRefs[weightIndex]}
            >
              -
            </button>
            <div className="orange-circle weight-circle">{weight}</div>
            <button
              className="step-btn weight-btn"
              onClick={() => onWeightUpdate(groupIndex, weightIndex, 1)}
              disabled={!canUpdateWeight(groupIndex, weightIndex, 1)}
            >
              +
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

function ConnectionLines({ inputRefs, weightRefs }) {
  const svgRef = useRef(null)
  const containerRef = useRef(null)
  const [lines, setLines] = useState([])

  useEffect(() => {
    const updateLines = () => {
      if (!containerRef.current || !svgRef.current) return

      const containerRect = containerRef.current.getBoundingClientRect()
      const newLines = []

      // For each input (0-3)
      for (let inputIdx = 0; inputIdx < 4; inputIdx++) {
        const inputRef = inputRefs[inputIdx]
        if (!inputRef?.current) continue

        const inputRect = inputRef.current.getBoundingClientRect()
        const inputCenterX = inputRect.left + inputRect.width / 2 - containerRect.left
        const inputCenterY = inputRect.top + inputRect.height / 2 - containerRect.top

        // Start a bit to the right of the input circle
        const inputX = inputCenterX + inputRect.width * 0.4
        const inputY = inputCenterY

        // Connect to corresponding weight group: endpoint near the left side of the '-' button
        for (let groupIdx = 0; groupIdx < 3; groupIdx++) {
          const weightRef = weightRefs[groupIdx]?.[inputIdx]
          if (!weightRef?.current) continue

          const weightRect = weightRef.current.getBoundingClientRect()
          const weightCenterY = weightRect.top + weightRect.height / 2 - containerRect.top

          // End slightly to the left of the '-' button's left edge
          const weightLeftX = weightRect.left - containerRect.left
          const weightX = weightLeftX - 4
          const weightY = weightCenterY

          newLines.push({
            id: `input${inputIdx}-group${groupIdx}-weight${inputIdx}`,
            x1: inputX,
            y1: inputY,
            x2: weightX,
            y2: weightY,
          })
        }
      }

      setLines(newLines)
    }

    // Initial update with delay to ensure layout is complete
    const initialTimeout = setTimeout(updateLines, 100)

    // Update on window resize
    window.addEventListener('resize', updateLines)

    // Use ResizeObserver to watch for layout changes
    const resizeObserver = new ResizeObserver(() => {
      setTimeout(updateLines, 50)
    })

    if (containerRef.current) {
      resizeObserver.observe(containerRef.current)
    }

    // Watch all input and weight elements
    inputRefs.forEach((ref) => {
      if (ref?.current) {
        resizeObserver.observe(ref.current)
      }
    })

    weightRefs.forEach((group) => {
      group.forEach((ref) => {
        if (ref?.current) {
          resizeObserver.observe(ref.current)
        }
      })
    })

    return () => {
      window.removeEventListener('resize', updateLines)
      clearTimeout(initialTimeout)
      resizeObserver.disconnect()
    }
  }, [inputRefs, weightRefs])

  return (
    <div ref={containerRef} className="connection-lines">
      <svg ref={svgRef}>
        {lines.map((line) => (
          <line
            key={line.id}
            x1={line.x1}
            y1={line.y1}
            x2={line.x2}
            y2={line.y2}
          />
        ))}
      </svg>
    </div>
  )
}

export default App
