function r2_display_table(T, fields, headers, precision)
% Format a report table without modifying the numerical results.
cells=cell(height(T)+1,numel(fields));
cells(1,:)=headers;
for j=1:numel(fields)
    v=T.(fields{j});
    for i=1:height(T)
        if isnumeric(v)
            value=v(i);
            if abs(value)<0.5*10^(-precision(j)), value=0; end
            cells{i+1,j}=sprintf('%.*f',precision(j),value);
        else
            cells{i+1,j}=char(r2_label(string(v(i))));
        end
    end
end
width=max(cellfun(@numel,cells),[],1);
for i=1:size(cells,1)
    for j=1:size(cells,2)
        fprintf('%-*s',width(j)+2,cells{i,j});
    end
    fprintf('\n');
end
end
