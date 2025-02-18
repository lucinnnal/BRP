import torch
import torchaudio
import os
from tqdm import tqdm

def compute_fbank_stats(audio_folder, target_length=1024, melbins=128):
    """
    Compute mean and standard deviation of mel-spectrograms from audio files in a folder
    
    Args:
        audio_folder (str): Path to folder containing audio files
        target_length (int): Target length of mel-spectrogram
        melbins (int): Number of mel bins
        
    Returns:
        tuple: (mean, std) of mel-spectrograms
    """
    # Initialize running statistics
    running_sum = 0
    running_square_sum = 0
    count = 0
    
    # Get list of wav files
    wav_files = [f for f in os.listdir(audio_folder) if f.endswith('.wav')]
    
    # Process each audio file
    for wav_file in tqdm(wav_files, desc="Computing statistics"):
        filepath = os.path.join(audio_folder, wav_file)
        
        # Load and preprocess audio
        waveform, sr = torchaudio.load(filepath)
        waveform = waveform - waveform.mean()
        
        # Compute mel-spectrogram
        try:
            fbank = torchaudio.compliance.kaldi.fbank(
                waveform, 
                htk_compat=True, 
                sample_frequency=sr, 
                use_energy=False, 
                window_type='hanning', 
                num_mel_bins=melbins, 
                dither=0.0, 
                frame_shift=10
            )
            
            # Handle padding/cutting
            n_frames = fbank.shape[0]
            p = target_length - n_frames
            
            if p > 0:
                m = torch.nn.ZeroPad2d((0, 0, 0, p))
                fbank = m(fbank)
            elif p < 0:
                fbank = fbank[0:target_length, :]
            
            # Update running statistics
            running_sum += torch.sum(fbank)
            running_square_sum += torch.sum(fbank ** 2)
            count += fbank.numel()
            
        except Exception as e:
            print(f'Error processing {wav_file}: {str(e)}')
            continue
    
    # Compute final statistics
    mean = running_sum / count
    std = torch.sqrt(running_square_sum / count - mean ** 2)
    
    return mean.item(), std.item()

if __name__ == "__main__":
    mean, std = compute_fbank_stats(audio_folder = "../preprocess/audio", target_length=1024, melbins=128)
    
    print(f"Dataset mean: {mean:.4f}")
    print(f"Dataset std: {std:.4f}")

    def normalize_fbank(fbank, mean, std):
        return (fbank - mean) / std