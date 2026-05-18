# Endogenous Rhythm Drive

无外部工程常数的内生参数自适应节律控制

## 安装

```bash
npm install
```

## 快速开始

运行演示实验：

```bash
npm test
```

这将在 `figures/` 目录下生成三个实验的 JSON 数据文件。

## 核心公式

### K₁/K₂二阶惯性

- `K₁ = |V_target - V_curr| / 40`
- `K₂ = 60 / V_curr`
- `Acceleration = (V_target - V_curr) × K₁ - (V_curr - V_target) × K₂`
- `V_next = V_curr + Acceleration × dt`

### SDAI自适应抑制

- `R = |V_inhibited - V_inhibitor| / V_inhibited`
- `InhibitionDamping = R × K₂_inhibited`
- `NetDrive = K₁_inhibited - InhibitionDamping`

### 心肺耦合

- `BreathBase = 20 - (V_curr - 60) × 6 / 40`
- `ConstraintForce = |BreathBase / BreathCurrent - 1| × K₂_current`

## 论文引用

```
@software{endogenous-rhythm-drive,
  author = {Chen Song},
  title = {Endogenous Parameter Second-Order Inertial Drive: The Adaptive Rhythm of PGI Digital Life},
  year = {2026},
  doi = {10.5281/zenodo.20237641}
}
```

## 许可证

CC BY-NC-SA 4.0
