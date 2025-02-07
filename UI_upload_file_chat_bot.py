import os
import shutil
import gradio as gr
import ans_extraction_from_faiss
import text_extraction_from_doc

# Directory to save the uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the directory exists

# Handle file upload and save it
def handle_file_upload(file):
    if file is None:
        return None, "Please upload a PPTX file!"

    # Save the uploaded file to the UPLOAD_DIR
    file_name = os.path.basename(file.name)
    file_extension = os.path.splitext(file_name)[1].lower()
    # move to the target directory
    saved_path = os.path.join(UPLOAD_DIR, file_name)
    shutil.move(file.name, saved_path)
    # call fun to store embedding:
    status = text_extraction_from_doc.process_presentation(file_extension,saved_path)
    if status == "Success":
        return saved_path, f"File '{file_name}' uploaded and Embedding calculated successfully!"

# Chatbot logic for responding based on the uploaded file
def chatbot_response(user_input, file_path):
    if not file_path:
        return "Please upload a PPTX/PDF file first to ask questions."

    try:
        # Use your custom logic to generate answers based on the file
        return ans_extraction_from_faiss.get_answer(user_input)
    except Exception as e:
        return f"Error while processing your question: {e}"

# Gradio Interface
with gr.Blocks() as ui:
    gr.Markdown("# 📁 Chatbot with File Upload")

    # File upload section
    file_path = gr.State(None)  # Store the processed file path
    with gr.Row():
        uploaded_file = gr.File(label="Upload PPTX")
        upload_button = gr.Button("Upload and Calculate Embeddings")

    upload_status = gr.Textbox(
        label="Embedding Status",
        placeholder=" status will appear here...",
        interactive=False
    )

    # Chatbot section
    user_input = gr.Textbox(
        placeholder="Ask a question about the file...",
        show_label=False,
        lines=1
    )
    send_button = gr.Button("Send")
    bot_response = gr.Textbox(
        label="Chatbot Response",
        placeholder="Bot's response will appear here...",
        interactive=False
    )

    # Link upload button to handle_file_upload
    upload_button.click(
        handle_file_upload,
        inputs=uploaded_file,
        outputs=[file_path, upload_status]
    )

    # Link send button to chatbot_response
    send_button.click(
        chatbot_response,
        inputs=[user_input, file_path],
        outputs=bot_response
    )

# Launch the chatbot UI
ui.launch()
