<style TYPE="text/css">
code.has-jax {font: inherit; font-size: 100%; background: inherit; border: inherit;}
</style>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
    tex2jax: {
        inlineMath: [['$','$'], ['\\(','\\)']],
        skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'] // removed 'code' entry
    }
});
MathJax.Hub.Queue(function() {
    var all = MathJax.Hub.getAllJax(), i;
    for(i = 0; i < all.length; i += 1) {
        all[i].SourceElement().parentNode.className += ' has-jax';
    }
});
</script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS_HTML-full"></script>

# 뭐에 관한 추측인지
이 추측은 자연수 k에 대해

$$ 
\sum ^{n}_{i=1}i^{k}=f\left( n\right) 
$$
를 만족하는 함수 f를 점진적으로 구하는 과정에 관한 것입니다.

<br/>
<br/>

# 추측
자연수 k, 다항함수 g(n)에 대해
$$
 \sum ^{n}_{i=1}i^{k}=g\left( n\right) 
 $$
가 성립한다고 가정하자. 그러면 다음이 성립한다.
$$
 \begin{aligned}\sum ^{n}_{i=1}\int _{0}^{i}t^{k}dt=\int ^{n}_{0}g\left( t\right) dt+Cn\\ C=\sum ^{1}_{i=1}\int ^{1}_{0}t^{k}dt-\int _{0}^{1}g\left( t\right) dt\end{aligned} 
 $$

