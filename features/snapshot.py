from pathlib import Path
import concurrent.futures
from moviepy.editor import VideoFileClip
from validations.overwrite import check_overwrite


class Snapshot:
    def __init__(self, files, f_output, f_interval, f_overwrite):
        self.files = files
        self.f_output = f_output
        self.f_interval = f_interval
        self.f_overwrite = f_overwrite

    def process_snapshot(self, file):
        video = VideoFileClip(str(file))
        video_duration = round(video.duration)

        for interval in range(0, video_duration, self.f_interval):
            new_filename = f'snapshot_{interval}_{str(file.name)}'.replace(
                str(file.suffix), '.jpg')

            # # We want snapshots of a video together in one folder, so the output doesn't become a mess.
            final_folder = self.f_output.joinpath(file.stem)
            Path(final_folder).mkdir(parents=True, exist_ok=True)

            final_output = final_folder.joinpath(new_filename)
            video.save_frame(f'{final_output}', t=interval)

            video.reader.close()
            video.audio.reader.close_proc()

    def snapshot_processor(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.process_snapshot, self.files)
