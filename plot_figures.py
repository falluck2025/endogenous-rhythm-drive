import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import os
import numpy as np

try:
    from scipy.interpolate import make_interp_spline
    def smooth_curve(x, y, num_points=500):
        x = np.array(x)
        y = np.array(y)
        x_smooth = np.linspace(x.min(), x.max(), num_points)
        spl = make_interp_spline(x, y, k=3)
        y_smooth = spl(x_smooth)
        return x_smooth, y_smooth
except ImportError:
    try:
        from scipy.interpolate import interp1d
        def smooth_curve(x, y, num_points=500):
            x = np.array(x)
            y = np.array(y)
            x_smooth = np.linspace(x.min(), x.max(), num_points)
            f = interp1d(x, y, kind='cubic')
            y_smooth = f(x_smooth)
            return x_smooth, y_smooth
    except ImportError:
        def smooth_curve(x, y, num_points=500):
            x = np.array(x)
            y = np.array(y)
            from scipy.interpolate import UnivariateSpline
            spl = UnivariateSpline(x, y, s=0.5)
            x_smooth = np.linspace(x.min(), x.max(), num_points)
            y_smooth = spl(x_smooth)
            return x_smooth, y_smooth

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(SCRIPT_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

with open(os.path.join(FIGURES_DIR, 'experiment1.json')) as f:
    data1 = json.load(f)

with open(os.path.join(FIGURES_DIR, 'experiment2.json')) as f:
    data2 = json.load(f)

with open(os.path.join(FIGURES_DIR, 'experiment3.json')) as f:
    data3 = json.load(f)

def generate_figure1():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    frames = [d['frame'] for d in data1]
    time_sec = [f / 60 for f in frames]
    v_curr = [d['V_curr'] for d in data1]
    
    time_smooth, v_smooth = smooth_curve(time_sec, v_curr)
    ax.plot(time_smooth, v_smooth, color='#1f4e78', linewidth=2, label='Endogenous K$_1$/K$_2$')
    
    fixed_step = [100.0] * len(time_sec)
    ax.plot(time_sec, fixed_step, color='gray', linewidth=1.5, linestyle='--', label='Fixed Step Linear')
    
    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_ylabel('Heart Rate (BPM)', fontsize=12)
    ax.set_title('K$_1$/K$_2$ Natural Overshoot Behavior', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.set_xlim([0, 5])
    ax.set_ylim([55, 110])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'figure1_overshoot.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print('Figure 1 saved: figure1_overshoot.png')

def generate_figure2():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])
    ax.axis('off')
    ax.set_title('Endogenous Rhythm vs External Clock Architecture', fontsize=14, fontweight='bold')
    
    left_box = mpatches.FancyBboxPatch((0.3, 5.5), 4.2, 3.5, 
                                        boxstyle="round,pad=0.1",
                                        facecolor='#E8F0FE', edgecolor='#1f4e78', linewidth=2)
    ax.add_patch(left_box)
    
    ax.text(2.4, 8.6, 'Endogenous Rhythm System', fontsize=12, ha='center', fontweight='bold', color='#1f4e78')
    ax.text(2.4, 7.8, 'K$_1$/K$_2$ Second-Order Inertial', fontsize=10, ha='center')
    ax.text(2.4, 7.2, 'SDAI Adaptive Inhibition Network', fontsize=10, ha='center')
    ax.text(2.4, 6.6, 'Cardiopulmonary Coupling', fontsize=10, ha='center')
    ax.text(2.4, 5.9, 'Self-Organized', fontsize=10, ha='center', fontweight='bold')
    ax.text(2.4, 5.4, 'No Central Controller', fontsize=9, ha='center')
    ax.text(2.4, 4.9, 'Emergent Coordination', fontsize=9, ha='center')
    
    right_box = mpatches.FancyBboxPatch((5.5, 5.5), 4.2, 3.5,
                                         boxstyle="round,pad=0.1",
                                         facecolor='#F0F0F0', edgecolor='#666666', linewidth=2)
    ax.add_patch(right_box)
    
    ax.text(7.6, 8.6, 'External Clock System', fontsize=12, ha='center', fontweight='bold', color='#666666')
    ax.text(7.6, 7.8, 'Fixed Step Size', fontsize=10, ha='center')
    ax.text(7.6, 7.2, 'Predefined Thresholds', fontsize=10, ha='center')
    ax.text(7.6, 6.6, 'Centralized Scheduling', fontsize=10, ha='center')
    ax.text(7.6, 5.9, 'Centralized Control', fontsize=10, ha='center', fontweight='bold')
    ax.text(7.6, 5.4, 'Fixed Timing', fontsize=9, ha='center')
    ax.text(7.6, 4.9, 'Scheduled Tasks', fontsize=9, ha='center')
    
    ax.annotate('', xy=(5.5, 7), xytext=(4.5, 7),
                arrowprops=dict(arrowstyle='->', color='green', lw=2.5))
    ax.text(5, 7.5, 'Natural\nAdapts', fontsize=9, ha='center', color='green', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'figure2_comparison.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print('Figure 2 saved: figure2_comparison.png')

def generate_figure3():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    frames = [d['frame'] for d in data1]
    time_sec = [f / 60 for f in frames]
    v_curr = [d['V_curr'] for d in data1]
    
    time_smooth, v_smooth = smooth_curve(time_sec, v_curr)
    ax.plot(time_smooth, v_smooth, color='#1f4e78', linewidth=2)
    
    fixed_step = [100.0] * len(time_sec)
    ax.plot(time_sec, fixed_step, color='gray', linewidth=1.5, linestyle='--', label='Fixed Step Linear')
    
    overshoot_idx = np.argmax(v_curr)
    overshoot_time = overshoot_idx / 60
    overshoot_value = max(v_curr)
    
    ax.annotate('Natural Overshoot',
                xy=(overshoot_time, overshoot_value),
                xytext=(overshoot_time - 0.8, overshoot_value + 6),
                fontsize=11,
                ha='center',
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8),
                color='red', fontweight='bold')
    
    convergence_time = None
    for i in range(50, len(v_curr) - 10):
        if abs(v_curr[i] - 100) < 0.5 and abs(v_curr[i+5] - 100) < 0.5:
            convergence_time = i / 60
            break
    if convergence_time:
        ax.annotate('Smooth Convergence',
                    xy=(convergence_time, 100),
                    xytext=(convergence_time + 1.5, 93),
                    fontsize=11,
                    ha='center',
                    arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.8),
                    color='green', fontweight='bold')
    
    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_ylabel('Heart Rate (BPM)', fontsize=12)
    ax.set_title('K$_1$/K$_2$ Natural Overshoot Curve with Peak Annotation', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.set_xlim([0, 5])
    ax.set_ylim([55, 110])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'figure3_overshoot_detail.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print('Figure 3 saved: figure3_overshoot_detail.png')

def generate_figure4():
    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    inhibition_levels = ['Strong\nInhibition', 'Medium\nInhibition', 'Weak\nInhibition']
    expected_r = [d['R'] for d in data2]
    actual_offset = [d['damping'] for d in data2]
    
    x = np.arange(len(inhibition_levels))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, expected_r, width, label='Expected R Value', color='#2e75b6', edgecolor='black')
    bars2 = ax.bar(x + width/2, actual_offset, width, label='Actual Offset (Damping)', color='#ff7f0e', edgecolor='black')
    
    ax.set_xlabel('Inhibition Level', fontsize=12)
    ax.set_ylabel('R Value / Damping', fontsize=12)
    ax.set_title('SDAI Response Verification - Inhibition Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(inhibition_levels, fontsize=10)
    ax.legend(loc='upper right', fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    for bar, val in zip(bars1, expected_r):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9)
    for bar, val in zip(bars2, actual_offset):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'figure4_sdai.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print('Figure 4 saved: figure4_sdai.png (unchanged)')

def generate_figure5():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('white')
    
    heart_data = data3['heartRateData']
    frames = [d['frame'] for d in heart_data]
    v_curr = [d['V_curr'] for d in heart_data]
    tasks = [d['tasks'] for d in heart_data]
    phases = [d['phase'] for d in heart_data]
    
    frames_smooth, v_smooth = smooth_curve(frames, v_curr)
    ax1.plot(frames_smooth, v_smooth, color='#1f4e78', linewidth=2, label='Heart Rate')
    
    ax1.axvline(x=50, color='gray', linestyle='--', linewidth=1)
    ax1.axvline(x=100, color='gray', linestyle='--', linewidth=1)
    ax1.text(25, 102, 'Light Load', fontsize=10, ha='center', fontweight='bold', color='green')
    ax1.text(75, 102, 'Heavy Load', fontsize=10, ha='center', fontweight='bold', color='red')
    ax1.text(125, 102, 'Recovery', fontsize=10, ha='center', fontweight='bold', color='green')
    
    ax1.set_ylabel('Heart Rate (BPM)', fontsize=12)
    ax1.set_title('Load Adaptation: Heart Rate and Throughput', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set_xlim([0, 150])
    ax1.set_ylim([55, 105])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    cumulative_tasks = np.cumsum(tasks)
    frames_cum = np.arange(len(cumulative_tasks))
    frames_cum_smooth, tasks_smooth = smooth_curve(frames_cum, cumulative_tasks)
    ax2.plot(frames_cum_smooth, tasks_smooth, color='#ff7f0e', linewidth=2)
    ax2.fill_between(frames_cum_smooth, tasks_smooth, alpha=0.3, color='#ff7f0e')
    
    ax2.axvline(x=50, color='gray', linestyle='--', linewidth=1)
    ax2.axvline(x=100, color='gray', linestyle='--', linewidth=1)
    
    ax2.set_xlabel('Frame (Time)', fontsize=12)
    ax2.set_ylabel('Throughput (tasks)', fontsize=12)
    ax2.legend(loc='upper right', fontsize=10)
    ax2.set_xlim([0, 150])
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'figure5_load.png'), bbox_inches='tight', facecolor='white')
    plt.close()
    print('Figure 5 saved: figure5_load.png')
    print(f'Total tasks processed: {int(cumulative_tasks[-1])}')

def main():
    print('Generating figures for Paper II...')
    print('=' * 50)
    
    generate_figure1()
    generate_figure2()
    generate_figure3()
    generate_figure4()
    generate_figure5()
    
    print('=' * 50)
    print('All 5 figures generated successfully!')
    print(f'Output directory: {FIGURES_DIR}')

if __name__ == '__main__':
    main()
