import gradio as gr


def calculate_result(input0, input1, input2, input3, weight0, weight1, weight2, weight3):
    """Calculate weighted sum: input0 * weight0 + input1 * weight1 + input2 * weight2 + input3 * weight3"""
    return (
        input0 * weight0
        + input1 * weight1
        + input2 * weight2
        + input3 * weight3
    )


def update_group(input0, input1, input2, input3, weight0, weight1, weight2, weight3, index, delta):
    """Increment/decrement one of the four weights and return updated value and weighted sum."""
    weights = [weight0, weight1, weight2, weight3]
    # Apply step and clamp between -3 and 3
    new_val = weights[index] + delta
    new_val = max(-3, min(3, new_val))
    weights[index] = new_val

    # Weighted sum with four inputs
    result = calculate_result(
        input0, input1, input2, input3, weights[0], weights[1], weights[2], weights[3]
    )
    return new_val, f"<div class='orange-circle'>{new_val}</div>", f"<div class='circle'>{result}</div>"


def bulk_update_group(
    input0,
    input1,
    input2,
    input3,
    weight0,
    weight1,
    weight2,
    weight3,
    delta_sign,
):
    """
    Update all four weights in a group by adding (or subtracting) the corresponding input values,
    then return updated weights, their circles, and the new group output.
    """
    weights = [weight0, weight1, weight2, weight3]
    inputs = [input0, input1, input2, input3]

    new_weights = []
    for w, x in zip(weights, inputs):
        new_w = w + delta_sign * x
        # clamp weights to a reasonable range
        new_w = max(-3, min(3, new_w))
        new_weights.append(new_w)

    result = calculate_result(
        input0, input1, input2, input3, new_weights[0], new_weights[1], new_weights[2], new_weights[3]
    )

    circles = [
        f"<div class='orange-circle'>{new_weights[0]}</div>",
        f"<div class='orange-circle'>{new_weights[1]}</div>",
        f"<div class='orange-circle'>{new_weights[2]}</div>",
        f"<div class='orange-circle'>{new_weights[3]}</div>",
    ]

    return (
        new_weights[0],
        new_weights[1],
        new_weights[2],
        new_weights[3],
        circles[0],
        circles[1],
        circles[2],
        circles[3],
        f"<div class='circle'>{result}</div>",
    )


def update_left_circle(
    input_state,
    input_index,
    delta,
    input0,
    input1,
    input2,
    input3,
    weight_0_0_state,
    weight_0_1_state,
    weight_0_2_state,
    weight_0_3_state,
    weight_1_0_state,
    weight_1_1_state,
    weight_1_2_state,
    weight_1_3_state,
    weight_2_0_state,
    weight_2_1_state,
    weight_2_2_state,
    weight_2_3_state,
):
    """Update left circle and recalculate all three result circles."""
    # Update the input value
    new_input = input_state + delta
    new_input = max(0, min(1, new_input))

    # Update the input values array with the new value
    inputs = [input0, input1, input2, input3]
    inputs[input_index] = new_input

    # Recalculate all three results using the updated input values
    result1 = calculate_result(
        inputs[0],
        inputs[1],
        inputs[2],
        inputs[3],
        weight_0_0_state,
        weight_0_1_state,
        weight_0_2_state,
        weight_0_3_state,
    )
    result2 = calculate_result(
        inputs[0],
        inputs[1],
        inputs[2],
        inputs[3],
        weight_1_0_state,
        weight_1_1_state,
        weight_1_2_state,
        weight_1_3_state,
    )
    result3 = calculate_result(
        inputs[0],
        inputs[1],
        inputs[2],
        inputs[3],
        weight_2_0_state,
        weight_2_1_state,
        weight_2_2_state,
        weight_2_3_state,
    )

    # Return the updated state value, the HTML circle, and all three result circles
    return (new_input, f"<div class='circle'>{new_input}</div>",
            f"<div class='circle'>{result1}</div>",
            f"<div class='circle'>{result2}</div>",
            f"<div class='circle'>{result3}</div>")


def build_interface():
    with gr.Blocks(css=custom_css(), title="Orange Box Layout") as demo:
        gr.Markdown("### Simple Gradio Layout with Centered Orange Box")

        with gr.Row(elem_classes="main-row"):
            # Left side numbers (inputs)
            with gr.Column(scale=1, elem_classes="side-column left-column"):
                with gr.Row(elem_classes="control-row"):
                    dec_input0 = gr.Button("-", elem_classes="step-btn")
                    circle_input0 = gr.HTML("<div class='circle'>0</div>")
                    inc_input0 = gr.Button("+", elem_classes="step-btn")

                with gr.Row(elem_classes="control-row"):
                    dec_input1 = gr.Button("-", elem_classes="step-btn")
                    circle_input1 = gr.HTML("<div class='circle'>1</div>")
                    inc_input1 = gr.Button("+", elem_classes="step-btn")

                with gr.Row(elem_classes="control-row"):
                    dec_input2 = gr.Button("-", elem_classes="step-btn")
                    circle_input2 = gr.HTML("<div class='circle'>2</div>")
                    inc_input2 = gr.Button("+", elem_classes="step-btn")

                with gr.Row(elem_classes="control-row"):
                    dec_input3 = gr.Button("-", elem_classes="step-btn")
                    circle_input3 = gr.HTML("<div class='circle'>3</div>")
                    inc_input3 = gr.Button("+", elem_classes="step-btn")

            # Center orange box
            with gr.Column(scale=2, elem_classes="center-column"):
                with gr.Column(elem_classes="orange-box"):
                    # First group of four controls
                    with gr.Row(elem_classes="control-group"):
                        with gr.Column(elem_classes="weight-controls"):
                            with gr.Row(elem_classes="control-row"):
                                dec_1_0 = gr.Button("-", elem_classes="step-btn")
                                circle_1_0 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_1_0 = gr.Button("+", elem_classes="step-btn")

                            with gr.Row(elem_classes="control-row"):
                                dec_1_1 = gr.Button("-", elem_classes="step-btn")
                                circle_1_1 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_1_1 = gr.Button("+", elem_classes="step-btn")

                            with gr.Row(elem_classes="control-row"):
                                dec_1_2 = gr.Button("-", elem_classes="step-btn")
                                circle_1_2 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_1_2 = gr.Button("+", elem_classes="step-btn")

                            with gr.Row(elem_classes="control-row"):
                                dec_1_3 = gr.Button("-", elem_classes="step-btn")
                                circle_1_3 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_1_3 = gr.Button("+", elem_classes="step-btn")
                        
                        with gr.Column(elem_classes="big-buttons-column"):
                            bulk_dec_0 = gr.Button("−", elem_classes="big-step-btn")
                            bulk_inc_0 = gr.Button("+", elem_classes="big-step-btn")

                    # Second group of four controls
                    with gr.Row(elem_classes="control-group"):
                        with gr.Column(elem_classes="weight-controls"):
                            with gr.Row(elem_classes="control-row"):
                                dec_2_0 = gr.Button("-", elem_classes="step-btn")
                                circle_2_0 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_2_0 = gr.Button("+", elem_classes="step-btn")

                            with gr.Row(elem_classes="control-row"):
                                dec_2_1 = gr.Button("-", elem_classes="step-btn")
                                circle_2_1 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_2_1 = gr.Button("+", elem_classes="step-btn")

                            with gr.Row(elem_classes="control-row"):
                                dec_2_2 = gr.Button("-", elem_classes="step-btn")
                                circle_2_2 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_2_2 = gr.Button("+", elem_classes="step-btn")

                            with gr.Row(elem_classes="control-row"):
                                dec_2_3 = gr.Button("-", elem_classes="step-btn")
                                circle_2_3 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_2_3 = gr.Button("+", elem_classes="step-btn")
                        
                        with gr.Column(elem_classes="big-buttons-column"):
                            bulk_dec_1 = gr.Button("−", elem_classes="big-step-btn")
                            bulk_inc_1 = gr.Button("+", elem_classes="big-step-btn")

                    # Third group of four controls
                    with gr.Row(elem_classes="control-group"):
                        with gr.Column(elem_classes="weight-controls"):
                            with gr.Row(elem_classes="control-row"):
                                dec_3_0 = gr.Button("-", elem_classes="step-btn")
                                circle_3_0 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_3_0 = gr.Button("+", elem_classes="step-btn")

                            with gr.Row(elem_classes="control-row"):
                                dec_3_1 = gr.Button("-", elem_classes="step-btn")
                                circle_3_1 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_3_1 = gr.Button("+", elem_classes="step-btn")

                            with gr.Row(elem_classes="control-row"):
                                dec_3_2 = gr.Button("-", elem_classes="step-btn")
                                circle_3_2 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_3_2 = gr.Button("+", elem_classes="step-btn")

                            with gr.Row(elem_classes="control-row"):
                                dec_3_3 = gr.Button("-", elem_classes="step-btn")
                                circle_3_3 = gr.HTML("<div class='orange-circle'>0</div>")
                                inc_3_3 = gr.Button("+", elem_classes="step-btn")
                        
                        with gr.Column(elem_classes="big-buttons-column"):
                            bulk_dec_2 = gr.Button("−", elem_classes="big-step-btn")
                            bulk_inc_2 = gr.Button("+", elem_classes="big-step-btn")

            # Right side numbers (outputs)
            with gr.Column(scale=1, elem_classes="side-column right-column"):
                output1 = gr.HTML("<div class='circle'>0</div>", elem_classes="result-circle")
                output2 = gr.HTML("<div class='circle'>0</div>", elem_classes="result-circle")
                output3 = gr.HTML("<div class='circle'>0</div>", elem_classes="result-circle")

        # Shared states for index and delta
        idx_0 = gr.State(0)  # For circle_0
        idx_1 = gr.State(1)  # For circle_1
        idx_2 = gr.State(2)  # For circle_2
        idx_3 = gr.State(3)  # For circle_3
        step_dec = gr.State(-1)
        step_inc = gr.State(1)
        
        # State components to track numeric values for left side inputs
        input0_state = gr.State(0)
        input1_state = gr.State(1)
        input2_state = gr.State(2)
        input3_state = gr.State(3)

        # State components to track numeric values for each weight in the box
        weight_0_0_state = gr.State(0)
        weight_0_1_state = gr.State(0)
        weight_0_2_state = gr.State(0)
        weight_0_3_state = gr.State(0)
        weight_1_0_state = gr.State(0)
        weight_1_1_state = gr.State(0)
        weight_1_2_state = gr.State(0)
        weight_1_3_state = gr.State(0)
        weight_2_0_state = gr.State(0)
        weight_2_1_state = gr.State(0)
        weight_2_2_state = gr.State(0)
        weight_2_3_state = gr.State(0)

        # --- Left side wiring ---
        input_idx_0 = gr.State(0)
        input_idx_1 = gr.State(1)
        input_idx_2 = gr.State(2)
        input_idx_3 = gr.State(3)

        # input0
        dec_input0.click(
            update_left_circle,
            inputs=[input0_state, input_idx_0, step_dec,
                    input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state],
            outputs=[input0_state, circle_input0, output1, output2, output3],
        )
        inc_input0.click(
            update_left_circle,
            inputs=[input0_state, input_idx_0, step_inc,
                    input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state],
            outputs=[input0_state, circle_input0, output1, output2, output3],
        )

        # input1
        dec_input1.click(
            update_left_circle,
            inputs=[input1_state, input_idx_1, step_dec,
                    input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state],
            outputs=[input1_state, circle_input1, output1, output2, output3],
        )
        inc_input1.click(
            update_left_circle,
            inputs=[input1_state, input_idx_1, step_inc,
                    input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state],
            outputs=[input1_state, circle_input1, output1, output2, output3],
        )

        # input2
        dec_input2.click(
            update_left_circle,
            inputs=[input2_state, input_idx_2, step_dec,
                    input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state],
            outputs=[input2_state, circle_input2, output1, output2, output3],
        )
        inc_input2.click(
            update_left_circle,
            inputs=[input2_state, input_idx_2, step_inc,
                    input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state],
            outputs=[input2_state, circle_input2, output1, output2, output3],
        )

        # input3
        dec_input3.click(
            update_left_circle,
            inputs=[input3_state, input_idx_3, step_dec,
                    input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state],
            outputs=[input3_state, circle_input3, output1, output2, output3],
        )
        inc_input3.click(
            update_left_circle,
            inputs=[input3_state, input_idx_3, step_inc,
                    input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state],
            outputs=[input3_state, circle_input3, output1, output2, output3],
        )

        # --- Group 1 wiring ---
        # bulk update group 0 (first row of weights)
        bulk_dec_0.click(
            bulk_update_group,
            inputs=[
                input0_state,
                input1_state,
                input2_state,
                input3_state,
                weight_0_0_state,
                weight_0_1_state,
                weight_0_2_state,
                weight_0_3_state,
                step_dec,
            ],
            outputs=[
                weight_0_0_state,
                weight_0_1_state,
                weight_0_2_state,
                weight_0_3_state,
                circle_1_0,
                circle_1_1,
                circle_1_2,
                circle_1_3,
                output1,
            ],
        )
        bulk_inc_0.click(
            bulk_update_group,
            inputs=[
                input0_state,
                input1_state,
                input2_state,
                input3_state,
                weight_0_0_state,
                weight_0_1_state,
                weight_0_2_state,
                weight_0_3_state,
                step_inc,
            ],
            outputs=[
                weight_0_0_state,
                weight_0_1_state,
                weight_0_2_state,
                weight_0_3_state,
                circle_1_0,
                circle_1_1,
                circle_1_2,
                circle_1_3,
                output1,
            ],
        )

        dec_1_0.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state, idx_0, step_dec],
            outputs=[weight_0_0_state, circle_1_0, output1],
        )
        inc_1_0.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state, idx_0, step_inc],
            outputs=[weight_0_0_state, circle_1_0, output1],
        )

        dec_1_1.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state, idx_1, step_dec],
            outputs=[weight_0_1_state, circle_1_1, output1],
        )
        inc_1_1.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state, idx_1, step_inc],
            outputs=[weight_0_1_state, circle_1_1, output1],
        )

        dec_1_2.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state, idx_2, step_dec],
            outputs=[weight_0_2_state, circle_1_2, output1],
        )
        inc_1_2.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state, idx_2, step_inc],
            outputs=[weight_0_2_state, circle_1_2, output1],
        )

        dec_1_3.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state, idx_3, step_dec],
            outputs=[weight_0_3_state, circle_1_3, output1],
        )
        inc_1_3.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_0_0_state, weight_0_1_state, weight_0_2_state, weight_0_3_state, idx_3, step_inc],
            outputs=[weight_0_3_state, circle_1_3, output1],
        )

        # --- Group 2 wiring ---
        # bulk update group 1 (second row of weights)
        bulk_dec_1.click(
            bulk_update_group,
            inputs=[
                input0_state,
                input1_state,
                input2_state,
                input3_state,
                weight_1_0_state,
                weight_1_1_state,
                weight_1_2_state,
                weight_1_3_state,
                step_dec,
            ],
            outputs=[
                weight_1_0_state,
                weight_1_1_state,
                weight_1_2_state,
                weight_1_3_state,
                circle_2_0,
                circle_2_1,
                circle_2_2,
                circle_2_3,
                output2,
            ],
        )
        bulk_inc_1.click(
            bulk_update_group,
            inputs=[
                input0_state,
                input1_state,
                input2_state,
                input3_state,
                weight_1_0_state,
                weight_1_1_state,
                weight_1_2_state,
                weight_1_3_state,
                step_inc,
            ],
            outputs=[
                weight_1_0_state,
                weight_1_1_state,
                weight_1_2_state,
                weight_1_3_state,
                circle_2_0,
                circle_2_1,
                circle_2_2,
                circle_2_3,
                output2,
            ],
        )

        dec_2_0.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state, idx_0, step_dec],
            outputs=[weight_1_0_state, circle_2_0, output2],
        )
        inc_2_0.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state, idx_0, step_inc],
            outputs=[weight_1_0_state, circle_2_0, output2],
        )

        dec_2_1.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state, idx_1, step_dec],
            outputs=[weight_1_1_state, circle_2_1, output2],
        )
        inc_2_1.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state, idx_1, step_inc],
            outputs=[weight_1_1_state, circle_2_1, output2],
        )

        dec_2_2.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state, idx_2, step_dec],
            outputs=[weight_1_2_state, circle_2_2, output2],
        )
        inc_2_2.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state, idx_2, step_inc],
            outputs=[weight_1_2_state, circle_2_2, output2],
        )

        dec_2_3.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state, idx_3, step_dec],
            outputs=[weight_1_3_state, circle_2_3, output2],
        )
        inc_2_3.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_1_0_state, weight_1_1_state, weight_1_2_state, weight_1_3_state, idx_3, step_inc],
            outputs=[weight_1_3_state, circle_2_3, output2],
        )

        # --- Group 3 wiring ---
        # bulk update group 2 (third row of weights)
        bulk_dec_2.click(
            bulk_update_group,
            inputs=[
                input0_state,
                input1_state,
                input2_state,
                input3_state,
                weight_2_0_state,
                weight_2_1_state,
                weight_2_2_state,
                weight_2_3_state,
                step_dec,
            ],
            outputs=[
                weight_2_0_state,
                weight_2_1_state,
                weight_2_2_state,
                weight_2_3_state,
                circle_3_0,
                circle_3_1,
                circle_3_2,
                circle_3_3,
                output3,
            ],
        )
        bulk_inc_2.click(
            bulk_update_group,
            inputs=[
                input0_state,
                input1_state,
                input2_state,
                input3_state,
                weight_2_0_state,
                weight_2_1_state,
                weight_2_2_state,
                weight_2_3_state,
                step_inc,
            ],
            outputs=[
                weight_2_0_state,
                weight_2_1_state,
                weight_2_2_state,
                weight_2_3_state,
                circle_3_0,
                circle_3_1,
                circle_3_2,
                circle_3_3,
                output3,
            ],
        )

        dec_3_0.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state, idx_0, step_dec],
            outputs=[weight_2_0_state, circle_3_0, output3],
        )
        inc_3_0.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state, idx_0, step_inc],
            outputs=[weight_2_0_state, circle_3_0, output3],
        )

        dec_3_1.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state, idx_1, step_dec],
            outputs=[weight_2_1_state, circle_3_1, output3],
        )
        inc_3_1.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state, idx_1, step_inc],
            outputs=[weight_2_1_state, circle_3_1, output3],
        )

        dec_3_2.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state, idx_2, step_dec],
            outputs=[weight_2_2_state, circle_3_2, output3],
        )
        inc_3_2.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state, idx_2, step_inc],
            outputs=[weight_2_2_state, circle_3_2, output3],
        )

        dec_3_3.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state, idx_3, step_dec],
            outputs=[weight_2_3_state, circle_3_3, output3],
        )
        inc_3_3.click(
            update_group,
            inputs=[input0_state, input1_state, input2_state, input3_state,
                    weight_2_0_state, weight_2_1_state, weight_2_2_state, weight_2_3_state, idx_3, step_inc],
            outputs=[weight_2_3_state, circle_3_3, output3],
        )

    return demo


def custom_css() -> str:
    return """
    .main-row {
        justify-content: center;
        align-items: center;
        height: 60vh;
    }

    .side-column {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 1.5rem;
        align-items: center;
    }

    .center-column {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .orange-box {
        width: 500px;
        height: 600px;
        background: #ff9800;
        border-radius: 12px;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.2);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        padding: 2rem;
    }

    .control-group {
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        width: auto;
    }
    
    .control-group:last-child {
        margin-bottom: 0;
    }

    .weight-controls {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        flex-shrink: 0;
    }

    .big-buttons-column {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 0.75rem;
        flex-shrink: 0;
        margin-left: 0;
    }

    .control-row {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        gap: 0.5rem;
        flex: 0 0 auto;
        width: auto;
    }

    .control-row > * {
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: 0;
    }
    
    .control-row .step-btn:first-child {
        margin-right: 0;
    }
    
    .control-row .step-btn:last-child {
        margin-left: 0;
    }

    .step-btn {
        min-width: 40px;
        max-width: 40px;
        height: 36px;
        padding: 0;
        font-size: 1.1rem;
        font-weight: 700;
        border-radius: 18px;
    }

    .big-step-btn {
        min-width: 60px;
        max-width: 60px;
        height: 40px;
        padding: 0;
        font-size: 1.2rem;
        font-weight: 800;
        border-radius: 20px;
    }

    .circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #ffffff;
        border: 3px solid #ff9800;
        color: #ff9800;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }
    
    .orange-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #ff9800;
        border: 3px solid #ffffff;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }

    @media (max-width: 768px) {
        .main-row {
            flex-direction: column;
            gap: 1.5rem;
        }

        .side-column {
            flex-direction: row;
        }

        .orange-box {
            width: 90%;
            max-width: 400px;
            height: 500px;
        }
    }
    """


if __name__ == "__main__":
    demo = build_interface()
    demo.launch()

