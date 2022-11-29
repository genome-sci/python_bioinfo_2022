library(tidyverse)

in_f <- ("output/count_tpm.tsv")
tpm <- read_table(in_f)
tpm_t <- data.table::transpose(tpm, make.names = 1)

rownames(tpm_t)
pca <-prcomp(tpm_t)
summary(pca)
# Importance of components:
#   PC1       PC2       PC3       PC4       PC5       PC6
# Standard deviation     7675.5957 3875.0885 2.929e+03 2.077e+03 1.738e+03 4.736e-11
# Proportion of Variance    0.6558    0.1671 9.547e-02 4.802e-02 3.362e-02 0.000e+00
# Cumulative Proportion     0.6558    0.8229 9.184e-01 9.664e-01 1.000e+00 1.000e+00

plotdf <- tibble(pc1 = pca$x[,1],
                 pc2 = pca$x[,2],
                 condition = c(1,1,1,2,2,2))

ggplot(plotdf,aes(x=pc1,y=pc2,color=condition))+
  geom_point() +
  theme(legend.position = "none") +
  geom_text(aes(x = pc1 + 200, label=colnames(tpm)[2:7]),hjust =0)+
  xlim(-7000, 14000)

