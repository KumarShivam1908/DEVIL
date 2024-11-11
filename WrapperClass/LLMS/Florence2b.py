import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image, ImageDraw
import cv2
import numpy as np
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import copy

class Florence2Detector:
    def __init__(self, model_id='microsoft/Florence-2-base'):
        """Initialize the Florence2 model."""
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, 
            trust_remote_code=True, 
            torch_dtype='auto'
        ).eval().cuda()
        self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
        self.colormap = ['blue','orange','green','purple','brown','pink','gray',
                        'olive','cyan','red','lime','indigo','violet','aqua',
                        'magenta','coral','gold','tan','skyblue']

    def predict(self, image, task_prompt='<OD>', text_input=None):
        """Run prediction on a single image."""
        if isinstance(image, str):
            image = Image.open(image).convert('RGB')
        elif isinstance(image, np.ndarray):
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        prompt = task_prompt if text_input is None else task_prompt + text_input
        
        inputs = self.processor(
            text=prompt, 
            images=image, 
            return_tensors="pt"
        ).to('cuda', torch.float16)

        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"].cuda(),
            pixel_values=inputs["pixel_values"].cuda(),
            max_new_tokens=1024,
            early_stopping=False,
            do_sample=False,
            num_beams=3,
        )

        generated_text = self.processor.batch_decode(
            generated_ids, 
            skip_special_tokens=False
        )[0]

        parsed_answer = self.processor.post_process_generation(
            generated_text,
            task=task_prompt,
            image_size=(image.width, image.height)
        )

        return parsed_answer, image

    def visualize_detection(self, image, results, output_path=None):
        """Visualize detection results."""
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(image)

        od_results = results.get('<OD>', {})
        for bbox, label in zip(od_results.get('bboxes', []), od_results.get('labels', [])):
            x1, y1, x2, y2 = bbox
            rect = patches.Rectangle(
                (x1, y1), x2-x1, y2-y1, 
                linewidth=2, 
                edgecolor='r', 
                facecolor='none'
            )
            ax.add_patch(rect)
            plt.text(
                x1, y1-5, 
                label, 
                color='white', 
                fontsize=10,
                bbox=dict(facecolor='red', alpha=0.5)
            )

        ax.axis('off')
        if output_path:
            plt.savefig(output_path)
            plt.close()
        else:
            plt.show()

    def draw_polygons(self, image, prediction, fill_mask=False):
        """Draw segmentation masks with polygons on an image."""
        draw = ImageDraw.Draw(image)
        
        for polygons, label in zip(prediction['polygons'], prediction['labels']):
            color = random.choice(self.colormap)
            fill_color = random.choice(self.colormap) if fill_mask else None

            for _polygon in polygons:
                _polygon = np.array(_polygon).reshape(-1, 2)
                if len(_polygon) < 3:
                    continue

                _polygon = _polygon.reshape(-1).tolist()

                if fill_mask:
                    draw.polygon(_polygon, outline=color, fill=fill_color)
                else:
                    draw.polygon(_polygon, outline=color)

                draw.text((_polygon[0] + 8, _polygon[1] + 2), label, fill=color)
        
        return image

    def process_image_detection(self, image_path, output_folder='output'):
        """Process image for object detection."""
        results, image = self.predict(image_path, task_prompt='<OD>')
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f"detected_{os.path.basename(image_path)}")
        self.visualize_detection(image, results, output_path)
        return results

    def process_image_segmentation(self, image_path, text_input, output_folder='output'):
        """Process image for segmentation."""
        results, image = self.predict(
            image_path, 
            task_prompt='<REFERRING_EXPRESSION_SEGMENTATION>', 
            text_input=text_input
        )
        os.makedirs(output_folder, exist_ok=True)
        
        output_image = copy.deepcopy(image)
        segmented_image = self.draw_polygons(
            output_image, 
            results['<REFERRING_EXPRESSION_SEGMENTATION>'], 
            fill_mask=True
        )
        
        output_path = os.path.join(output_folder, f"segmented_{os.path.basename(image_path)}")
        segmented_image.save(output_path)
        return results, segmented_image

    def process_video_detection(self, video_path, output_folder='output', frame_step=1):
        """Process video for object detection."""
        os.makedirs(output_folder, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(output_folder, f"{base_name}_detected.mp4")

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        
        with tqdm(total=total_frames) as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % frame_step == 0:
                    results, _ = self.predict(frame, task_prompt='<OD>')
                    
                    od_results = results.get('<OD>', {})
                    for bbox, label in zip(od_results.get('bboxes', []), od_results.get('labels', [])):
                        x1, y1, x2, y2 = map(int, bbox)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                out.write(frame)
                frame_count += 1
                pbar.update(1)

        cap.release()
        out.release()
        print(f"Processed video saved to: {output_path}")

    def process_video_segmentation(self, video_path, text_input, output_folder='output', frame_step=1):
        """Process video for segmentation."""
        os.makedirs(output_folder, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(output_folder, f"{base_name}_segmented.mp4")

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        
        with tqdm(total=total_frames) as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % frame_step == 0:
                    results, _ = self.predict(
                        frame,
                        task_prompt='<REFERRING_EXPRESSION_SEGMENTATION>',
                        text_input=text_input
                    )
                    
                    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    segmented_image = self.draw_polygons(
                        pil_image, 
                        results['<REFERRING_EXPRESSION_SEGMENTATION>'], 
                        fill_mask=True
                    )
                    frame = cv2.cvtColor(np.array(segmented_image), cv2.COLOR_RGB2BGR)

                out.write(frame)
                frame_count += 1
                pbar.update(1)

        cap.release()
        out.release()
        print(f"Processed video saved to: {output_path}")

